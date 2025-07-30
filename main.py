import json
import csv
import io # NEW: Import io for in-memory CSV writing
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
from groq import Groq

# --- Global variable to store last processed tasks (for CSV export) ---
last_processed_tasks_for_csv = []

# --- LLM System Prompt ---
llm_system_prompt = """
You are an intelligent and meticulous **Project Task Management AI Assistant**. Your primary goal is to transform raw, often messy and unstructured, task descriptions into clear, actionable, and organized entries. This process is crucial for busy project managers who need to quickly grasp and prioritize their workload.

For each individual task description provided, you MUST perform the following three core operations accurately and systematically:

1.  **Summarize (Concise and Clear):** Extract the absolute essence of the task and distill it into a very short, clear, and actionable summary. This summary MUST be no more than 15 words, designed for immediate understanding and quick scanning. Store this in the 'summary' field.

2.  **Auto-Tag (Relevant Keywords):** Identify the most relevant overarching themes or categories for the task. You MUST assign **exactly 1 or 2 tags** per task. Prioritize using common project management tags like #urgent, #bug, #feature, #meeting, #documentation, #research, #marketing, #client, #backend, #frontend, #design, #devops, #qa, #followup, #presentation, #refactor. If a highly relevant tag is not on this list, you may infer a new, concise, and appropriate tag. Store these as an array of strings in the 'tags' field.

3.  **Assign Priority Score (1-5 Scale):** Evaluate the task's urgency, its potential impact on the project or client, and its overall importance. Assign a numerical priority score from 1 to 5, where:
    * **5 = Highest Priority:** Critical, urgent, blocking, or immediate client impact.
    * **4 = High Priority:** Important, needs prompt attention, significant impact.
    * **3 = Medium Priority:** Standard importance, planned work, routine follow-up.
    * **2 = Low Priority:** Minor task, can be deferred, minimal immediate impact.
    * **1 = Lowest Priority:** Backlog item, very low impact, purely optional.
    Store this as an integer in the 'priority' field.

Your final output MUST be a **valid JSON array**. Each element within this array MUST be a JSON object structured precisely as follows:
{
    \"original_task\": \"[The full, original messy task description you received]\",
    \"summary\": \"[Your concise summary (max 15 words)]\",
    \"tags\": [\"#tag1\", \"#tag2\"],
    \"priority\": [1-5 numerical score]
}

Ensure there are no leading or trailing spaces, extra characters, or conversational text outside of the JSON array. **Provide ONLY the JSON array in your response.**

Now, please process the following list of tasks:
"""

# --- Real LLM API Call (using Groq) ---
def call_llm_api(tasks_list_str, system_prompt):
    """
    Makes an actual API call to an LLM (Groq) to process tasks.
    """
    llm_response_content = "" # Initialize to ensure it's always defined
    try:
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        print("\n--- Calling Groq API... (This might take a few seconds) ---")

        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192", # Or "mixtral-8x7b-32768" or "llama3-70b-8192"
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Tasks:\n{tasks_list_str}",
                },
            ],
            temperature=0.7,
        )

        llm_response_content = chat_completion.choices[0].message.content
        print(f"\n--- Raw LLM Response Content ---\n{llm_response_content}\n----------------------------------") # Debug print
        
        parsed_response = json.loads(llm_response_content)
        print(f"\n--- Parsed LLM Response (Python Object) ---\n{parsed_response}\n-------------------------------------------") # Debug print
        return parsed_response

    except Exception as e: # Catching general exceptions for API errors, network issues, etc.
        print(f"\n--- ERROR During Groq API Call ---")
        print(f"An error occurred: {e}")
        print("\nPlease check your GROQ_API_KEY environment variable, internet connection, and Groq API usage limits.")
        if llm_response_content: # Check if content was received before parsing failed
            print(f"Raw response content that caused error: {llm_response_content}")
        print("----------------------------------\n")
        return []

# --- Core Task Processing Logic ---
def smart_task_summarizer(tasks_list):
    # Ensure tasks_list is a list of strings
    if not isinstance(tasks_list, list):
        tasks_list = [tasks_list.strip()] if isinstance(tasks_list, str) else []
    
    # Filter out any empty strings from the list
    tasks_list = [task.strip() for task in tasks_list if task.strip()]

    if not tasks_list:
        print("\n--- No valid tasks provided for summarization. ---")
        return [] # Return empty if no valid tasks

    tasks_str = "\n".join([f"- {task}" for task in tasks_list])
    
    # CALLING THE REAL GROQ API
    processed_tasks = call_llm_api(tasks_str, llm_system_prompt)
    
    # NEW: Store the processed tasks globally for CSV export
    global last_processed_tasks_for_csv
    last_processed_tasks_for_csv = processed_tasks

    return processed_tasks

# --- HTML Generation Functions ---
def generate_task_card_html(task):
    """Generates the HTML for a single processed task card."""
    tags_html = "".join([
        f'<span class="tag">{tag}</span>' for tag in task.get('tags', [])
    ])

    priority = task.get('priority', 0)
    priority_class = ""
    if priority == 5: priority_class = "priority-5"
    elif priority == 4: priority_class = "priority-4"
    elif priority == 3: priority_class = "priority-3"
    elif priority == 2: priority_class = "priority-2"
    elif priority == 1: priority_class = "priority-1"
    else: priority_class = "bg-gray-500" # Default if priority is not 1-5

    return f"""
    <div class="task-card">
        <p>Original: {task.get('original_task', 'N/A')}</p>
        <h3>Summary: {task.get('summary', 'N/A')}</h3>
        <div class="tags-container">
            {tags_html}
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge {priority_class}">
                {priority}/5
            </span>
        </div>
    </div>
    """

def generate_processed_results_html(processed_tasks):
    """Generates the full HTML block for all processed tasks."""
    if not processed_tasks:
        return "<p style='color: #aaaaaa; text-align: center;'>No tasks processed or an error occurred. Please check the server logs for details.</p>"

    cards_html = "".join([
        generate_task_card_html(task) for task in processed_tasks
    ])

    return f"""
    <h2>Processed Tasks</h2>
    <div class="tasks-list">
        {cards_html}
    </div>
    """

# --- HTTP Server Handler ---
class SimpleTaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            self.wfile.write(html_content.encode('utf-8'))
        
        elif path == '/download_csv':
            # Check if there are tasks to export
            if not last_processed_tasks_for_csv:
                self.send_response(404) # Not Found if no data
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("No processed tasks to download. Please process tasks first.".encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/csv')
            self.send_header('Content-Disposition', 'attachment; filename="processed_tasks.csv"')
            self.end_headers()

            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(['Original Task', 'Summary', 'Tags', 'Priority'])

            for task in last_processed_tasks_for_csv:
                original_task = task.get('original_task', 'N/A')
                summary = task.get('summary', 'N/A')
                tags = ", ".join(task.get('tags', []))
                priority = task.get('priority', 0)
                writer.writerow([original_task, summary, tags, priority])
            
            csv_content = output.getvalue()
            output.close()

            self.wfile.write(csv_content.encode('utf-8'))
        
        else:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            parsed_data = parse_qs(post_data)
            raw_tasks_input = parsed_data.get('tasks_input', [''])[0]

            tasks_list = [task.strip() for task in raw_tasks_input.split('\n') if task.strip()]
            
            # Check if API key is set before calling LLM
            if not os.getenv("GROQ_API_KEY"):
                error_html = "<p style='color: red; text-align: center;'>ERROR: GROQ_API_KEY environment variable not set. Please set it to use the API.</p>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('index.html', 'r', encoding='utf-8') as f:
                    base_html_content = f.read()
                final_html_response = base_html_content.replace(
                    '<div id="processed-results"></div>',
                    f'<div id="processed-results">{error_html}</div>'
                )
                self.wfile.write(final_html_response.encode('utf-8'))
                return # Stop processing if key is missing

            processed_tasks = smart_task_summarizer(tasks_list)
            
            print(f"\n--- Processed Tasks (Python Object) After LLM Call ---\n{processed_tasks}\n----------------------------------------------------")
            
            results_html = generate_processed_results_html(processed_tasks)
            
            print(f"\n--- Generated Results HTML String ---\n{results_html}\n-------------------------------------")

            with open('index.html', 'r', encoding='utf-8') as f:
                base_html_content = f.read()

            final_html_response = base_html_content.replace(
                '<div id="processed-results"></div>',
                f'<div id="processed-results">{results_html}</div>'
            )
            
            start_idx = final_html_response.find('<div id="processed-results">')
            end_idx = final_html_response.find('</body>', start_idx)
            if start_idx != -1 and end_idx != -1:
                print(f"\n--- Final HTML Response (Snippet around results) ---\n{final_html_response[start_idx:end_idx]}\n--------------------------------------------------")
            else:
                print("\n--- Could not find processed-results div or body tag in final HTML. ---")


            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(final_html_response.encode('utf-8'))
        else:
            self.send_error(404, "File Not Found: %s" % self.path)

# --- Run the HTTP Server ---
def run_server(server_class=HTTPServer, handler_class=SimpleTaskHandler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"--- Starting Smart Task Summarizer Web App (Plain HTML/Python Server with Groq) ---")
    print(f"Open your web browser and go to http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("--- Server Stopped ---")

if __name__ == '__main__':
    run_server()