# FloraOS: The Intelligent Bloom - Autonomous Urban Garden Management System

![resized floraos_official](https://github.com/user-attachments/assets/8a8359be-a0af-42d6-a9af-a5aafb523832)

The Smart Garden Automation System, FloraOS, is an intelligent platform for urban garden management, built using Google's Agent Development Kit (ADK). It demonstrates the power of multi-agent systems to automate complex environmental monitoring and decision-making processes. FloraOS coordinates weather, soil health, and plant vision data to provide actionable insights and simulated automated responses for gardeners, showcasing how sophisticated automation, typically seen in robotics or IT, can be applied to biological and environmental systems. This project directly addresses the "Automation of Complex Processes" challenge by designing a multi-agent workflow to manage the intricate tasks of urban gardening.

## ✨ Features & Functionality

**Overview:** FloraOS automates the monitoring and management of a simulated urban garden by orchestrating specialized agents that gather diverse environmental data, analyze it, and determine appropriate actions.

**Detailed Breakdown & Agent Orchestration:**

FloraOS employs a multi-agent system where each agent has a distinct role, communicating and collaborating via ADK to automate the garden management workflow:

1.  **SoilSensorAgent:**
    *   **Function:** Simulates reading and publishing crucial soil sensor data.
    *   **Data:** Generates or reads from a predefined dataset (CSV/JSON) mimicking soil conditions (moisture %, pH, nutrient levels - NPK). This data is structured similarly to an IoT Core message payload.
    *   **Output:** Publishes structured soil data (e.g., `{ "timestamp": "...", "location": "Bed A", "moisture": 45.2, "ph": 6.5, "nitrogen": 10, "phosphorus": 5, "potassium": 8 }`).
    *   **Automation Role:** Provides foundational ground-truth data for decision-making.

2.  **WeatherAgent:**
    *   **Function:** Fetches current weather conditions and short-term forecast data.
    *   **Data:** Uses a public API (e.g., OpenWeatherMap) for real-time data or a simulated forecast dataset for reliability.
    *   **Output:** Publishes structured weather data (e.g., `{ "timestamp": "...", "location": "Garden Area", "temp_c": 22.0, "humidity": 60, "precipitation_prob_next_12h": 0.1, "uv_index": 5 }`).
    *   **Automation Role:** Introduces external environmental factors into the decision matrix.

3.  **PlantVisionAgent:**
    *   **Function:** Analyzes simulated images of plants to assess their health status.
    *   **Data:** Takes pre-selected image files representing different plant states (healthy, wilting, nutrient deficient, pest infestation).
    *   **GCP Integration:** Utilizes **Google Cloud Vertex AI Vision API** (a Custom Classification model trained on example images) to classify the plant's condition.
    *   **Output:** Publishes plant health assessment (e.g., `{ "timestamp": "...", "plant_id": "Tomato Plant 1", "image_ref": "sim_img_001.jpg", "status": "Needs Water", "confidence": 0.85 }`).
    *   **Automation Role:** Adds a sophisticated perception layer, enabling direct assessment of plant well-being.

4.  **GardenControlAgent (The "Brain"):**
    *   **Function:** Subscribes to data streams from the SoilSensorAgent, WeatherAgent, and PlantVisionAgent. It applies decision logic to determine necessary actions for garden management.
    *   **Decision Logic (MVP):** Rule-based. Examples:
        *   `IF SoilSensorAgent.moisture < threshold AND WeatherAgent.precipitation_prob_next_12h < low_threshold AND PlantVisionAgent.status == "Needs Water" THEN trigger watering.`
        *   `IF PlantVisionAgent.status == "Potential Nutrient Deficiency" THEN trigger specific nutrient delivery.`
        *   `IF SoilSensorAgent.ph outside optimal range THEN recommend pH adjustment action.`
    *   **Output:** Publishes simulated actuation commands (e.g., `{ "timestamp": "...", "action": "ACTIVATE_WATERING", "target": "Bed A", "duration_minutes": 5 }`).
    *   **Automation Role:** Orchestrates the overall process by consuming information from specialized agents, making intelligent decisions, and dispatching commands, thus automating a complex multi-step feedback loop.

**Problem Solved:**
Managing urban gardens or similar environmental systems involves continuously monitoring diverse, dynamic data sources (soil conditions, weather patterns, plant health indicators) and coordinating timely actions (watering, nutrient application, pest control). Performing these tasks manually is labor-intensive, inefficient, and often suboptimal. FloraOS automates this complex process by:
*   Continuously gathering and structuring disparate data.
*   Applying intelligent logic to interpret this data in context.
*   Automatically determining and dispatching (simulated) corrective actions.
This showcases an end-to-end automated workflow for environmental management.

## 🛠️ Tech Stack 

*   **Core Orchestration:** Google Agent Development Kit (ADK)
*   **Programming Language:** Python 3.7+
*   **Google Cloud Platform (GCP):**
    *   **Vertex AI Vision:** For image-based plant health classification by the PlantVisionAgent (Custom Image Classification Model).
    *   *(Conceptual Link for future extension: Cloud IoT Core for real-world sensor integration, Cloud Functions for serverless agent logic).*
*   **APIs:** OpenWeatherMap API (for WeatherAgent)
*   **Data Handling:** JSON (for inter-agent messages), CSV/JSON (for simulated sensor data).
*   **Version Control:** Git

**Google ADK Integration:**
ADK is the central nervous system of FloraOS.
*   **Agent Registration & Discovery:** Agents register with the ADK runtime.
*   **Message Bus (Pub/Sub):** Clear message schemas and topics (e.g., `garden/soil_data`, `garden/weather_data`, `garden/plant_health`, `garden/control_actions`) are defined for inter-agent communication. Agents publish their data to specific topics, and other agents (like the GardenControlAgent) subscribe to relevant data streams.
*   **Orchestration of Workflows:** ADK facilitates the flow of information and the sequence of operations, enabling the GardenControlAgent to react to combined inputs from multiple specialized agents. The demo explicitly shows messages being passed and the system reacting autonomously.

## 📊 Data Sources

*   **Soil Data:** Simulated data generated by the `SoilSensorAgent` or read from local CSV/JSON files. This data is curated based on horticultural knowledge to represent various soil states (e.g., optimal, dry, nutrient-deficient).
*   **Weather Data:**
    *   **Primary:** Real-time weather data fetched from the OpenWeatherMap API by the `WeatherAgent`.
    *   **Fallback:** Simulated weather data read from local JSON files for offline testing and controlled demo scenarios.
*   **Plant Image Data:** A curated library of local image files (`.jpg`, `.png`) representing different plant health conditions (healthy, wilting, nutrient-deficient). These images are fed to the `PlantVisionAgent` for analysis via Vertex AI. Images were sourced from public datasets (e.g., Kaggle selections) and organized for model training and agent input.

## 💡 Findings & Learnings

*   **Power of Specialization:** Breaking down a complex problem like garden management into specialized agent roles significantly simplifies development and allows for more focused intelligence within each agent.
*   **ADK for Orchestration:** ADK proved to be an effective framework for managing communication and dependencies between agents, making the development of the overall workflow more structured.
*   **Vertex AI for Perception:** Integrating Vertex AI for plant image analysis was straightforward and added a powerful, real-world AI capability to the system, showcasing how advanced perception can be incorporated into agent workflows.
*   **Data is Key:** The quality and structure of simulated data (especially for soil and initial plant health states) were critical for effectively training the PlantVision model and for demonstrating meaningful decision-making by the GardenControlAgent. Curating data based on domain knowledge, even when simulated, greatly enhances the realism and impact of the demo.
*   **Challenge - Time Constraint:** Integrating multiple components (ADK, multiple agents, GCP services) within a short hackathon timeframe required strict prioritization (MVP first) and parallel development where possible. Having clear message schemas early on was crucial.
*   **Learning - Asynchronous Nature:** Managing the asynchronous arrival of data from different agents and ensuring the GardenControlAgent makes decisions based on a coherent state of the garden requires careful design.

## 🏛️ Architecture Diagram (Conceptual Description)

FloraOS is architected as a distributed multi-agent system orchestrated by Google ADK.

1.  **Input Agents (Data Producers):**
    *   **SoilSensorAgent:** Reads from a local CSV/JSON data file (simulating IoT sensor inputs) and publishes structured soil data (moisture, pH, NPK) to an ADK topic (e.g., `garden/soil_data`).
    *   **WeatherAgent:** Fetches data from the OpenWeatherMap API (or a local JSON file) and publishes structured weather data (temperature, humidity, precipitation forecast) to an ADK topic (e.g., `garden/weather_data`).
    *   **PlantVisionAgent:**
        *   Takes a path to a local image file as input (simulating a camera capture).
        *   Sends this image to a **Google Cloud Vertex AI Vision endpoint** (Custom Image Classification Model).
        *   Receives the classification result (e.g., "Needs Water," "Healthy").
        *   Publishes a structured plant health assessment to an ADK topic (e.g., `garden/plant_health`).

2.  **Central Orchestrator & Decision-Maker:**
    *   **Google ADK Runtime:** Acts as the message bus and registry for all agents. It facilitates the publish/subscribe communication pattern.
    *   **GardenControlAgent (The Brain):**
        *   Subscribes to the `garden/soil_data`, `garden/weather_data`, and `garden/plant_health` topics via ADK.
        *   Internally aggregates the latest data from these sources.
        *   Applies a set of predefined rules (decision logic) based on the combined state of the garden.
        *   Publishes (simulated) actuation commands (e.g., "ACTIVATE_WATERING," "DEPLOY_NUTRIENTS") to an ADK topic (e.g., `garden/control_actions`).

3.  **Output/Actuation (Simulated):**
    *   (Conceptual) An "ActuatorAgent" or a simple logger could subscribe to `garden/control_actions` to display the commands determined by the GardenControlAgent, thus demonstrating the completion of the automated loop.

**Data Flow:** Data flows from specialized sensor/perception agents through ADK to the central GardenControlAgent, which then dispatches action commands back through ADK. This forms a closed-loop automated system.

## 🚀 Getting Started / Setup

**Prerequisites:**

*   Python 3.7+
*   `pip` (Python package installer)
*   Google Cloud SDK (`gcloud` CLI) installed and authenticated (for Vertex AI interaction).
*   A Google Cloud Project with Billing enabled and the Vertex AI API enabled.
*   An OpenWeatherMap API Key (free tier is sufficient).
*   Git for cloning the repository.
*   Access to install Google ADK (refer to official ADK documentation for installation).

**Installation Steps:**

1.  **Clone the Repository:**
    ```bash
    git clone [Insert URL to your public GitHub repository here]
    cd flora-os # Or your repository's root directory
    ```

2.  **Set up a Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    A `requirements.txt` file should be present in the repository.
    ```bash
    pip install -r requirements.txt
    pip install google-adk # Or the specific ADK package name
    ```
    *Note: Ensure `google-cloud-aiplatform` is in your `requirements.txt` for Vertex AI.*

4.  **Set Up Environment Variables:**
    You will need to configure API keys and GCP project details. Create a `.env` file in the root directory or in specific agent directories as required by your setup.
    *   **For WeatherAgent:**
        ```
        OPENWEATHER_API_KEY=your_openweathermap_api_key_here
        ```
    *   **For PlantVisionAgent (and GCP access):**
        Ensure your `gcloud` CLI is authenticated to the correct project, or set the following environment variables if running in an environment without implicit `gcloud` auth:
        ```
        GOOGLE_APPLICATION_CREDENTIALS=path/to/your-gcp-service-account-key.json # If using a service account
        GCP_PROJECT_ID=your-gcp-project-id
        GCP_REGION=your-gcp-region # e.g., us-central1
        VERTEX_AI_ENDPOINT_ID=your-vertex-ai-plant-classifier-endpoint-id
        ```

5.  **Prepare Data:**
    *   Ensure the simulated soil data (e.g., `soil_data.csv`) is in the expected location for the `SoilSensorAgent`.
    *   Ensure the curated plant images are available for the `PlantVisionAgent`.
    *   If using simulated weather data as a fallback, ensure the `weather_data.json` file is present.

## ⚙️ Usage

FloraOS is typically run by starting each agent. The agents will then communicate via ADK. You'll observe their interactions primarily through console logs, which will show published messages, received data, and decisions made by the `GardenControlAgent`.

1.  **Start the ADK Runtime/Broker:** (Depending on your specific ADK setup, this might be a separate step or handled when agents connect).

2.  **Run Each Agent:**
    Open separate terminal windows for each agent. Navigate to the agent's directory (if structured that way) or run them from the root.

    *   **Start SoilSensorAgent:**
        ```bash
        python agents/soilsensor_agent/agent.py # Adjust path as per your structure
        ```
    *   **Start WeatherAgent:**
        ```bash
        python agents/weather_agent/agent.py # Adjust path
        ```
    *   **Start PlantVisionAgent:**
        This agent might be triggered to process an image or run in a loop processing a list of images.
        ```bash
        python agents/plantvision_agent/agent.py # Adjust path
        ```
    *   **Start GardenControlAgent:**
        ```bash
        python agents/gardencontrol_agent/agent.py # Adjust path
        ```

3.  **Observe the System:**
    *   Watch the console output of each agent.
    *   You should see the `SoilSensorAgent` and `WeatherAgent` publishing data periodically.
    *   When the `PlantVisionAgent` processes an image, it will log its call to Vertex AI and the resulting health assessment.
    *   The `GardenControlAgent` will log the data it receives from other agents.
    *   When conditions in the (simulated) garden meet the criteria for one of its rules, the `GardenControlAgent` will log the triggered rule and the (simulated) action command it publishes (e.g., "ACTIVATE_WATERING").

**Example Demo Scenario:**
1.  Ensure `SoilSensorAgent` publishes data indicating low moisture (e.g., `moisture: 25`).
2.  Ensure `WeatherAgent` publishes data indicating a low probability of rain (e.g., `precipitation_prob_next_12h: 0.05`).
3.  Trigger `PlantVisionAgent` with an image of a wilting plant. Vertex AI should classify it as "Needs Water."
4.  Observe the `GardenControlAgent` receive these three pieces of information and trigger its "watering" rule, publishing an "ACTIVATE_WATERING" command.

## 🔗 Project Links

*   **Hosted Project:** [Insert URL to your deployed FloraOS application here - *If not applicable, state "The project is designed to be run locally. Please see GitHub repository for setup."*]
*   **Public Code Repository:** [Insert URL to your public GitHub repository here]
*   **Demonstration Video:** [Insert URL to your YouTube or Vimeo demo video here]

## 💡 Optional Developer Contributions

*(Fill this section if applicable, otherwise remove or state "N/A")*

*   **Demo Video:**
    *   [Link to your content] - 
*   **ADK Open-Source Contribution:**
    *   [Link to your GitHub profile/commit/PR/issue]

## 👥 Team / Resources

*   **Team:**
    *   AI PM & AI/ML Engineer (Chichi)
    *   Lead AI/ML Engineer (Susree)
    *   Software Engineer (Rohit)
*   **Resources:**
    *   Thanks to Google for providing the Agent Development Kit and hosting this hackathon.
    *   OpenWeatherMap for their weather API.
    *   Wikimedia Commons used for training the PlantVisionAgent.


