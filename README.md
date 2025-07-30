Smart Task Summarizer + Tagger
AI Engineer Intern Task Submission
Overview
This utility is designed to assist busy project managers by streamlining the process of organizing unstructured task descriptions from various sources (e.g., meetings, calls, client notes). It leverages AI to automatically summarize, tag, and prioritize tasks, transforming raw input into clear, actionable, and organized entries.

The solution includes a dynamic web interface for user input and output display, powered by a Python backend that integrates with a live LLM API.

Core Functionality
Dynamic Task Input (Web UI): Users can paste multiple messy, unstructured task descriptions into a web form.

AI Processing (Live LLM): The backend utilizes a Large Language Model (LLM) to perform three key operations on each submitted task:

Summarization: Condenses each task into a short, clear, and actionable summary (max 15 words).

Auto-Tagging: Assigns 1 to 2 relevant tags (e.g., #urgent, #frontend, #client) to categorize the task.

Priority Scoring: Assigns a numerical priority score (1-5, where 5 is highest) based on urgency, impact, and importance.

Dynamic Web Output: The final cleaned-up task list, including the summary, tags, and priority score, is displayed directly on the webpage below the input form.

CSV Export: A "Download as CSV" button allows users to export the currently processed tasks into a structured CSV file for easy integration with other tools or record-keeping.

Tools Used
AI: Groq API (using models like llama3-8b-8192) for live Large Language Model processing.

Backend/Logic: Python 3.x and its built-in http.server module for creating the web server and handling data processing.

Frontend/Interface: Plain HTML and CSS for a simple, responsive, and clean web user interface.

How the AI Prompt was Designed
The LLM prompt (llm_system_prompt in task_summarizer.py) was meticulously crafted to ensure accurate, consistent, and structured JSON output from the AI. Key design principles included:

Clear Role Definition: The LLM is explicitly instructed to act as an "intelligent and meticulous Project Task Management AI Assistant," setting a precise context for its operations.

Explicit Task Breakdown: The prompt clearly outlines the three core operations (summarize, auto-tag, assign priority) that the LLM must perform for each task.

Strict Output Format: A crucial instruction mandates the output to be a valid JSON array, with each element being a JSON object conforming to a predefined schema (original_task, summary, tags, priority). An example JSON object is provided to eliminate ambiguity.

Guiding Constraints & Definitions:

A maximum word count (15 words) is specified for summaries to ensure conciseness.

A preferred list of common project management tags is provided, guiding the LLM towards relevant categorization while allowing for inference of new, appropriate tags.

A detailed legend for the 1-5 priority scale is included, explaining the criteria (urgency, impact, importance) for each score.

Clean Output Instruction: The prompt explicitly directs the LLM to provide only the JSON array in its response, preventing any extraneous conversational text or characters that could interfere with programmatic parsing.

Screenshot / Terminal Output
(IMPORTANT: Replace this section with your actual terminal output and a screenshot of your working web application. You can paste the terminal output directly here, and for the screenshot, you might need to host it online or include it as a separate file in your submission.)

--- Starting Smart Task Summarizer Web App (Plain HTML/Python Server with Groq) ---
Open your web browser and go to http://127.0.0.1:8000/
127.0.0.1 - - [30/Jul/2025 15:30:38] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jul/2025 15:30:38] code 404, message File Not Found: /favicon.ico
127.0.0.1 - - [30/Jul/2025 15:30:38] "GET /favicon.ico HTTP/1.1" 404 -
--- Calling Groq API... (This might take a few seconds) ---
--- Raw LLM Response Content ---
[
    {
        "original_task": "Client needs urgent response about the website's new login bug affecting premium users. It's stopping conversions. ETA ASAP!",
        "summary": "Urgent client bug: login issue affecting premium users, high conversion impact.",
        "tags": ["#urgent", "#bug", "#client"],
        "priority": 5
    },
    {
        "original_task": "Schedule a meeting with the design team to review the new dashboard mockups. Need to get feedback before Monday's client demo.",
        "summary": "Schedule design review meeting for dashboard mockups before client demo.",
        "tags": ["#meeting", "#design"],
        "priority": 4
    },
    {
        "original_task": "Investigate the reported API rate limit issues on the user authentication service. Some users are getting 429 errors.",
        "summary": "Investigate API rate limit errors in user authentication service.",
        "tags": ["#bug", "#backend"],
        "priority": 4
    },
    {
        "original_task": "Write documentation for the new payment gateway integration. Make sure to cover both dev and admin setup. Due next sprint.",
        "summary": "Create documentation for new payment gateway, covering dev and admin setup.",
        "tags": ["#documentation", "#feature"],
        "priority": 3
    },
    {
        "original_task": "Refactor the old CSS files in the 'contact-us' page. They are very messy and causing some rendering issues on mobile. Low priority.",
        "summary": "Refactor messy CSS on contact-us page, fixing mobile rendering issues.",
        "tags": ["#frontend", "#refactor"],
        "priority": 2
    },
    {
        "original_task": "Follow up with Sarah from marketing regarding the social media campaign assets for next month. She promised them last week.",
        "summary": "Follow up with Marketing for next month's social media campaign assets.",
        "tags": ["#followup", "#marketing"],
        "priority": 3
    },
    {
        "original_task": "Research potential third-party libraries for PDF generation in Python. Looking for something robust and scalable.",
        "summary": "Research robust Python libraries for scalable PDF generation.",
        "tags": ["#research", "#backend"],
        "priority": 2
    },
    {
        "original_task": "Prepare a brief presentation on Q2 project achievements for the internal team meeting on Friday. Highlight key wins and challenges.",
        "summary": "Prepare Q2 project achievements presentation for internal team meeting.",
        "tags": ["#presentation", "#meeting"],
        "priority": 3
    }
]
----------------------------------
--- Parsed LLM Response (Python Object) ---
[{'original_task': 'Client needs urgent response about the website\'s new login bug affecting premium users. It\'s stopping conversions. ETA ASAP!', 'summary': 'Urgent client bug: login issue affecting premium users, high conversion impact.', 'tags': ['#urgent', '#bug', '#client'], 'priority': 5}, {'original_task': 'Schedule a meeting with the design team to review the new dashboard mockups. Need to get feedback before Monday\'s client demo.', 'summary': 'Schedule design review meeting for dashboard mockups before client demo.', 'tags': ['#meeting', '#design'], 'priority': 4}, {'original_task': 'Investigate the reported API rate limit issues on the user authentication service. Some users are getting 429 errors.', 'summary': 'Investigate API rate limit errors in user authentication service.', 'tags': ['#bug', '#backend'], 'priority': 4}, {'original_task': 'Write documentation for the new payment gateway integration. Make sure to cover both dev and admin setup. Due next sprint.', 'summary': 'Create documentation for new payment gateway, covering dev and admin setup.', 'tags': ['#documentation', '#feature'], 'priority': 3}, {'original_task': 'Refactor the old CSS files in the \'contact-us\' page. They are very messy and causing some rendering issues on mobile. Low priority.', 'summary': 'Refactor messy CSS on contact-us page, fixing mobile rendering issues.', 'tags': ['#frontend', '#refactor'], 'priority': 2}, {'original_task': 'Follow up with Sarah from marketing regarding the social media campaign assets for next month. She promised them last week.', 'summary': 'Follow up with Marketing for next month\'s social media campaign assets.', 'tags': ['#followup', '#marketing'], 'priority': 3}, {'original_task': 'Research potential third-party libraries for PDF generation in Python. Looking for something robust and scalable.', 'summary': 'Research robust Python libraries for scalable PDF generation.', 'tags': ['#research', '#backend'], 'priority': 2}, {'original_task': 'Prepare a brief presentation on Q2 project achievements for the internal team meeting on Friday. Highlight key wins and challenges.', 'summary': 'Prepare Q2 project achievements presentation for internal team meeting.', 'tags': ['#presentation', '#meeting'], 'priority': 3}]
-------------------------------------------
--- Processed Tasks (Python Object) After LLM Call ---
[{'original_task': 'Client needs urgent response about the website\'s new login bug affecting premium users. It\'s stopping conversions. ETA ASAP!', 'summary': 'Urgent client bug: login issue affecting premium users, high conversion impact.', 'tags': ['#urgent', '#bug', '#client'], 'priority': 5}, {'original_task': 'Schedule a meeting with the design team to review the new dashboard mockups. Need to get feedback before Monday\'s client demo.', 'summary': 'Schedule design review meeting for dashboard mockups before client demo.', 'tags': ['#meeting', '#design'], 'priority': 4}, {'original_task': 'Investigate the reported API rate limit issues on the user authentication service. Some users are getting 429 errors.', 'summary': 'Investigate API rate limit errors in user authentication service.', 'tags': ['#bug', '#backend'], 'priority': 4}, {'original_task': 'Write documentation for the new payment gateway integration. Make sure to cover both dev and admin setup. Due next sprint.', 'summary': 'Create documentation for new payment gateway, covering dev and admin setup.', 'tags': ['#documentation', '#feature'], 'priority': 3}, {'original_task': 'Refactor the old CSS files in the \'contact-us\' page. They are very messy and causing some rendering issues on mobile. Low priority.', 'summary': 'Refactor messy CSS on contact-us page, fixing mobile rendering issues.', 'tags': ['#frontend', '#refactor'], 'priority': 2}, {'original_task': 'Follow up with Sarah from marketing regarding the social media campaign assets for next month. She promised them last week.', 'summary': 'Follow up with Marketing for next month\'s social media campaign assets.', 'tags': ['#followup', '#marketing'], 'priority': 3}, {'original_task': 'Research potential third-party libraries for PDF generation in Python. Looking for something robust and scalable.', 'summary': 'Research robust Python libraries for scalable PDF generation.', 'tags': ['#research', '#backend'], 'priority': 2}, {'original_task': 'Prepare a brief presentation on Q2 project achievements for the internal team meeting on Friday. Highlight key wins and challenges.', 'summary': 'Prepare Q2 project achievements presentation for internal team meeting.', 'tags': ['#presentation', '#meeting'], 'priority': 3}]
----------------------------------------------------
--- Generated Results HTML String ---
    <h2>Processed Tasks</h2>
    <div class="tasks-list">
        
    <div class="task-card">
        <p>Original: Client needs urgent response about the website's new login bug affecting premium users. It's stopping conversions. ETA ASAP!</p>
        <h3>Summary: Urgent client bug: login issue affecting premium users, high conversion impact.</h3>
        <div class="tags-container">
            <span class="tag">#urgent</span><span class="tag">#bug</span><span class="tag">#client</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-5">
                5/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Schedule a meeting with the design team to review the new dashboard mockups. Need to get feedback before Monday's client demo.</p>
        <h3>Summary: Schedule design review meeting for dashboard mockups before client demo.</h3>
        <div class="tags-container">
            <span class="tag">#meeting</span><span class="tag">#design</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-4">
                4/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Investigate the reported API rate limit issues on the user authentication service. Some users are getting 429 errors.</p>
        <h3>Summary: Investigate API rate limit errors in user authentication service.</h3>
        <div class="tags-container">
            <span class="tag">#bug</span><span class="tag">#backend</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-4">
                4/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Write documentation for the new payment gateway integration. Make sure to cover both dev and admin setup. Due next sprint.</p>
        <h3>Summary: Create documentation for new payment gateway, covering dev and admin setup.</h3>
        <div class="tags-container">
            <span class="tag">#documentation</span><span class="tag">#feature</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Refactor the old CSS files in the 'contact-us' page. They are very messy and causing some rendering issues on mobile. Low priority.</p>
        <h3>Summary: Refactor messy CSS on contact-us page, fixing mobile rendering issues.</h3>
        <div class="tags-container">
            <span class="tag">#frontend</span><span class="tag">#refactor</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-2">
                2/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Follow up with Sarah from marketing regarding the social media campaign assets for next month. She promised them last week.</p>
        <h3>Summary: Follow up with Marketing for next month's social media campaign assets.</h3>
        <div class="tags-container">
            <span class="tag">#followup</span><span class="tag">#marketing</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Research potential third-party libraries for PDF generation in Python. Looking for something robust and scalable.</p>
        <h3>Summary: Research robust Python libraries for scalable PDF generation.</h3>
        <div class="tags-container">
            <span class="tag">#research</span><span class="tag">#backend</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-2">
                2/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Prepare a brief presentation on Q2 project achievements for the internal team meeting on Friday. Highlight key wins and challenges.</p>
        <h3>Summary: Prepare Q2 project achievements presentation for internal team meeting.</h3>
        <div class="tags-container">
            <span class="tag">#presentation</span><span class="tag">#meeting</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    </div>
-------------------------------------
--- Final HTML Response (Snippet around results) ---
<div id="processed-results">
    <h2>Processed Tasks</h2>
    <div class="tasks-list">
        
    <div class="task-card">
        <p>Original: Client needs urgent response about the website's new login bug affecting premium users. It's stopping conversions. ETA ASAP!</p>
        <h3>Summary: Urgent client bug: login issue affecting premium users, high conversion impact.</h3>
        <div class="tags-container">
            <span class="tag">#urgent</span><span class="tag">#bug</span><span class="tag">#client</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-5">
                5/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Schedule a meeting with the design team to review the new dashboard mockups. Need to get feedback before Monday's client demo.</p>
        <h3>Summary: Schedule design review meeting for dashboard mockups before client demo.</h3>
        <div class="tags-container">
            <span class="tag">#meeting</span><span class="tag">#design</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-4">
                4/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Investigate the reported API rate limit issues on the user authentication service. Some users are getting 429 errors.</p>
        <h3>Summary: Investigate API rate limit errors in user authentication service.</h3>
        <div class="tags-container">
            <span class="tag">#bug</span><span class="tag">#backend</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-4">
                4/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Write documentation for the new payment gateway integration. Make sure to cover both dev and admin setup. Due next sprint.</p>
        <h3>Summary: Create documentation for new payment gateway, covering dev and admin setup.</h3>
        <div class="tags-container">
            <span class="tag">#documentation</span><span class="tag">#feature</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Refactor the old CSS files in the 'contact-us' page. They are very messy and causing some rendering issues on mobile. Low priority.</p>
        <h3>Summary: Refactor messy CSS on contact-us page, fixing mobile rendering issues.</h3>
        <div class="tags-container">
            <span class="tag">#frontend</span><span class="tag">#refactor</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-2">
                2/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Follow up with Sarah from marketing regarding the social media campaign assets for next month. She promised them last week.</p>
        <h3>Summary: Follow up with Marketing for next month's social media campaign assets.</h3>
        <div class="tags-container">
            <span class="tag">#followup</span><span class="tag">#marketing</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Research potential third-party libraries for PDF generation in Python. Looking for something robust and scalable.</p>
        <h3>Summary: Research robust Python libraries for scalable PDF generation.</h3>
        <div class="tags-container">
            <span class="tag">#research</span><span class="tag">#backend</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-2">
                2/5
            </span>
        </div>
    </div>
    
    <div class="task-card">
        <p>Original: Prepare a brief presentation on Q2 project achievements for the internal team meeting on Friday. Highlight key wins and challenges.</p>
        <h3>Summary: Prepare Q2 project achievements presentation for internal team meeting.</h3>
        <div class="tags-container">
            <span class="tag">#presentation</span><span class="tag">#meeting</span>
        </div>
        <div class="priority-display">
            <span>Priority:</span>
            <span class="priority-badge priority-3">
                3/5
            </span>
        </div>
    </div>
    
    </div>