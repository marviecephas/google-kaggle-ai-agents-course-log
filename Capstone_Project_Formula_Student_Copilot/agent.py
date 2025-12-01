import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import preload_memory
from google.adk.apps.app import App, ResumabilityConfig
from typing import List, Dict, Any

# ==========================================
# 1. KNOWLEDGE BASE (Rules Agent)
# ==========================================
# Comprehensive dictionary derived from "fsuk-2026-rules---v1-0_copy.pdf"

FORMULA_RULES_DATABASE = {
    "Powertrain": {
        "Engine Limitation": "The engine used must be a piston engine utilizing a four-stroke primary heat cycle with a displacement not exceeding 710 cm³ per cycle.",
        "Starter Requirement": "Each vehicle must be equipped with an on-board starter, which must be used to start the vehicle.",
        "Air Intake Location": "All parts of the engine air and fuel control systems must lie within the Surface Envelope. Portions less than 350mm above ground must be protected from impacts.",
        "Intake Restrictor Requirement": "A single circular restrictor must be placed in the intake system, and all engine airflow must pass through it. The restricting cross section may not be movable or flexible in any way.",
        "Restrictor Diameter (Gasoline)": "Maximum restrictor diameter for gasoline fuelled vehicles is 20mm.",
        "Restrictor Diameter (E85)": "Maximum restrictor diameter for E85 fuelled vehicles is 19mm.",
        "Turbocharger Configuration": "For turbocharged or supercharged engines, the component sequence must be: restrictor, compressor, throttle body, engine.",
        "Plenum Restriction": "Plenums anywhere upstream of the throttle body are prohibited.",
        "Crankcase Venting": "Any crankcase or engine lubrication vent lines routed to the intake system must be connected upstream of the intake system restrictor.",
        "Coolant Fluid": "Water-cooled engines must only use plain water.",
        "Catch Can Requirement (Volume)": "Separate catch cans are required for engine coolant and engine lubrication systems. Each must have a minimum volume of 10% of the contained fluid or 900ml, whichever is greater.",
        "Catch Can Venting": "Catch cans must vent through a hose with a minimum internal diameter of 3mm down to the chassis bottom level and must exit outside the bodywork.",
        "Mechanical Throttle Springs": "If mechanical throttle actuation is used, it must use at least two return springs located at the throttle body, capable of returning the throttle to the idle position even if one fails.",
        "ETC Sensors (if used)": "If Electronic Throttle Control (ETC) is used, it must be equipped with at least Accelerator Pedal Position Sensors (APPSs), two Throttle Position Sensors (TPSs), and one Brake System Encoder (BSE).",
        "ETC Failure Response": "When power is removed, the electronic throttle must immediately close to idle position ±5%. Failure to close within one second must result in immediate disabling of power to ignition, fuel injectors, and fuel pump.",
        "Fuel Type": "Basic fuels available are unleaded gasoline (Sustainable 95RON E10 and 99RON E5) and E85. Vehicles must be operated with the fuel provided at the competition.",
        "Fuel System Location": "All parts of the fuel storage and supply system must lie within the Surface Envelope. In side view, no portion can project below the lower surface of the chassis.",
        "Fuel System Clearance": "All parts of the fuel system must be located at least 50mm from any exhaust system component.",
        "Fuel System Shielding": "Portions of the fuel system less than 350mm above the ground must be shielded from front, side, and rear impact collisions by a fully triangulated structure meeting T3.2 or equivalent.",
        "Filler Neck and Sight Tube": "The filler neck must have an inner diameter of at least 35mm. A clear, fuel resistant sight tube, at least 125mm vertical height, must be present above the top of the fuel tank.",
        "Fuel Level Line": "A permanent, clear, and easily visible fuel level line must be located between 12mm and 25mm below the top of the visible portion of the sight tube.",
        "Fuel Vent Requirement": "All fuel vent lines must be equipped with a check valve to prevent leakage when the tank is inverted and must exit outside the bodywork.",
        "Exhaust Routing": "The exhaust outlet must be routed to the side or rear, and must not extend more than 450mm behind the rear axle centreline and be no more than 600mm above the ground.",
        "Exhaust Insulation Prohibition": "The application of fibrous/absorbent material (e.g., 'header wrap') to the outside of an exhaust manifold or system is prohibited.",
        "Max Noise Level (High Speed)": "Maximum sound level up to an average piston speed of 15.25m/s is 110dB(C), fast weighting.",
        "Max Noise Level (Idle)": "Maximum permitted sound level at idle speed is 103dB(C), fast weighting.",
        "Intake Air Tightness Test": "After passing the noise test, the air tightness of the intake system will be tested by closing off the inlet, after which the engine must stall."
    },
    
    "Suspension_and_Brake_System": {
        "Suspension Travel": "Front and rear suspension must have a usable wheel travel of at least 50mm and a minimum jounce of 25 mm with the driver seated.",
        "Minimum Ground Clearance": "Minimum static ground clearance of any portion of the vehicle, other than the tyres, including a driver, must be 30mm.",
        "Brake System General": "The vehicle must have a hydraulic brake system acting on all four wheels and operated by a single control.",
        "Brake Circuits": "The system must have two independent hydraulic circuits such that effective braking is maintained on at least two wheels upon failure.",
        "Brake By Wire Prohibition": "Brake-by-wire systems are prohibited in manual mode.",
        "Brake Over-Travel Switch (BOTS)": "A BOTS must be installed as part of the shutdown circuit, opening the circuit if there is a failure in at least one brake circuit.",
        "Brake Light": "A single red brake light must illuminate if and only if the hydraulic brake system is actuated.",
        "Wheel Nut Retention": "Any wheel mounting system using a single retaining nut must incorporate a device to retain the nut and the wheel if the nut loosens.",
        "Tyres": "Vehicles must have dry tyres and wet tyres (minimum tread depth of 2.4 mm). Tyre warmers are prohibited.",
        "Steering Mechanism": "The steering wheel must directly mechanically actuate the front wheels. Steering systems using cables or belts are prohibited."
    },
    
    "Drivetrain": {
        "Transmission Type": "Any transmission and drivetrain may be used.",
        "Vehicle Movement": "Movement of the vehicle without a person in the vehicle and with the master switch(es) in the off position must be possible.",
        "Scatter Shields Requirement": "Exposed rotating final drivetrain parts (chains, belts, and brake discs not mounted within a wheel) must be fitted with scatter shields.",
        "Scatter Shield Material (Metal)": "Scatter shields for metallic chains/brake discs must be 2mm steel.",
        "Scatter Shield Material (Non-metal)": "Scatter shields for non-metallic belts must be 3mm aluminium alloy 6061-T6.",
        "Scatter Shield Fasteners": "Scatter shields must be attached with 6mm metric grade 8.8 or stronger fasteners."
    },
    
    "Chassis": {
        "Mandatory Structures": "The vehicle structure must include: Two braced Roll Hoops, a Front Bulkhead (FB) with support system and Impact Attenuator (IA), and Side Impact Structures (SIS).",
        "Minimum Steel Material (Hoops)": "Main and front hoops must use round steel tubing with a minimum wall thickness of 2.0mm.",
        "Main Hoop Construction": "The main hoop must be constructed of a single piece of uncut, continuous, closed section steel tubing.",
        "Front Hoop Angling": "In side view, no part of the front hoop can be inclined more than 20° from vertical.",
        "Impact Attenuator Dimensions": "The IA must be at least 100mm high and 200mm wide for a minimum distance of 200mm forward of the front bulkhead.",
        "Anti-Intrusion Plate (AIP) Material": "The AIP must be 1.5mm solid steel or 4.0mm solid aluminium.",
        "Impact Attenuator Performance": "The IA assembly must absorb at least 7350 J and decelerate a 300 kg vehicle at 7 m/s at a rate not exceeding 20g average and 40g peak.",
        "SES Submission": "All teams must submit a Structural Equivalency Spreadsheet (SES). Fabrication must adhere to the materials and processes described in the approved SES.",
        "Cockpit Egress": "All drivers must be able to exit to the side of the vehicle in less than 5 seconds.",
        "Firewall Separation": "A firewall must separate the driver compartment from all fuel supply systems, engine oil, liquid cooling systems, and the low voltage battery.",
        "Firewall Material": "The firewall must be a non-permeable surface made from a rigid, fire-retardant material.",
        "Harness Attachment Load": "Shoulder and lap belt attachments must support 13kN; anti-submarine belts must support 6.5kN."
    },
    
    "Electronics_and_Control": {
        "Low Voltage Limit": "Maximum permitted voltage in the Low Voltage System (LVS) is 60 V DC or 25 V AC RMS.",
        "LVMS Function": "The Low Voltage Master Switch (LVMS) must completely disable power from the Low Voltage (LV) battery and the alternator to the LVS.",
        "LVMS Location/Type": "The LVMS must be a mechanical rotary switch with a red, removable handle. It must be located on the right side of the vehicle, near the main hoop, at the driver’s shoulder height.",
        "Shutdown Circuit Components (CV)": "The shutdown circuit is a series connection of at least the LVMS, the BSPD, three shutdown buttons, the BOTS, and the inertia switch.",
        "Shutdown Actuation": "The shutdown circuit directly controls all electrical power to the ignition, fuel injectors and all fuel pumps, acting through a minimum of two mechanical relays.",
        "Inertia Switch Trigger": "The inertia switch must trigger due to an omnidirectional peak acceleration of ≤8 g (for ≥50ms pulse) and ≤13g (for ≥20ms pulse).",
        "BSPD Activation (CV)": "The Brake System Plausibility Device (BSPD) must open the shutdown circuit when hard braking occurs AND the throttle position is more than 25% over idle position for more than 500ms.",
        "Critical Fasteners Standard": "All threaded critical fasteners must be at least 4mm metric grade 8.8 or SAE Grade 5 or equivalent.",
        "Fastener Locking": "All critical fasteners must be secured from unintentional loosening by positive locking mechanisms (e.g., safety wiring, cotter pins)."
    },
    
    "Aerodynamics": {
        "Device Definition": "A structure designed to guide airflow, increasing downforce and/or lowering drag. Powered devices (e.g., fans) to move air from *under* the vehicle are prohibited.",
        "Max Height Forward": "Aerodynamic devices forward of the driver head restraint support must be lower than 500mm from the ground.",
        "Max Height Rearward": "All aerodynamic devices rearward of the driver head restraint support must be lower than 1.1m from the ground.",
        "Max Length Forward": "Devices must not extend further forward than 700mm from the fronts of the front tyres.",
        "Max Length Rearward": "Devices must not extend further rearward than 250mm from the rearmost part of the rear tyres.",
        "Edge Radii": "All forward facing horizontal edges must have a minimum radius of 5mm, and vertical edges must have a minimum radius of 3mm.",
        "Strength Test 1": "Devices must withstand 200N distributed over 225cm² and not deflect more than 10mm.",
        "Strength Test 2": "Devices must withstand 50N applied in any direction and not deflect more than 25mm."
    },
    
    "Drafting": {
        "Wheel-to-Wheel Prohibition": "Teams must never use their vehicles for wheel-to-wheel races.",
        "Endurance Passing Procedure": "During the endurance event, overtaking is only permissible in designated passing zones and under the control of the track marshals. A slower vehicle shown the blue flag must drive into the slow lane and decelerate.",
        "Blue Flag": "If a driver is shown a blue flag, they must pull into the designated passing zone."
    },
    
    "Business": {
        "Business Plan Objective": "The objective is to assess the team’s ability to present a comprehensive business model for a monetary profit, based on the prototype vehicle or a core component.",
        "BPP Format": "The presentation is a maximum of 10 minutes followed by a 5 minute Q&A. Penalties apply if the presentation is less than 9 minutes or exceeds 11 minutes.",
        "Cost Objective": "Evaluate the team’s understanding of manufacturing processes, costs, and greenhouse gas emissions (GHG) associated with construction.",
        "Cost Documentation": "Requires submission of the Bill of Material file (BOM), Supporting Material file, and Cost & Emissions Explanation file (CRD). A minimum of one hard copy of all CRD must be brought to the event.",
        "CCBOM Content": "The Costed Carbonised Bill of Material (CCBOM) must include actual manufacturing processes, tooling, costs, and the system’s carbon footprint in kg CO2e. Costs must be displayed in EUR.",
        "Design Objective": "Evaluate the student’s engineering process, understanding and effort in designing a vehicle meeting the competition intent.",
        "EDR Length": "The Engineering Design Report (EDR) must not exceed eight (8) pages total: five (5) pages of content (text/images) and three (3) pages of drawings.",
        "Design Penalties": "Up to 50 penalty points may be given for a fundamental lack of engineering knowledge, lack of design justification, or use of ‘carry-over parts’.",
        "LTS Purpose": "The Lap Time Simulation (LTS) event requires submission of an optimal vehicle parameter set and a Model Validation Test Plan report (max 2 pages)."
    }
}

# ==========================================
# 2. TOOLS
# ==========================================

def get_rules_from_db(category: str) -> Dict[str, Any]:
    """Retrieves all rules for a specific category from the database."""
    category_cleaned = category.replace(" ", "_")
    if category_cleaned in FORMULA_RULES_DATABASE:
        return FORMULA_RULES_DATABASE[category_cleaned]
    
    # Fuzzy match
    for key in FORMULA_RULES_DATABASE.keys():
        if category.lower() in key.lower():
            return FORMULA_RULES_DATABASE[key]
            
    return {
        "error": f"Category '{category}' not found.",
        "valid_categories": list(FORMULA_RULES_DATABASE.keys())
    }

def add_team_task(tool_context: ToolContext, task: str) -> str:
    """Adds a task to the current session's task list."""
    tasks = tool_context.state.get("tasks", [])
    tasks.append(task)
    tool_context.state["tasks"] = tasks
    return f"Task '{task}' added to database."

def view_team_tasks(tool_context: ToolContext) -> List[str]:
    """Views all tasks in the current session."""
    return tool_context.state.get("tasks", [])

def confirm_suggestion(tool_context: ToolContext, original_task: str, suggested_replacement: str, reason: str) -> dict:
    """Pauses execution to ask for human approval of a design change."""
    # Resume logic
    if tool_context.tool_confirmation:
        if tool_context.tool_confirmation.confirmed:
            return {"status": "APPROVED", "message": f"User approved. Proceeding with: '{suggested_replacement}'."}
        else:
            return {"status": "REJECTED", "message": "User rejected."}

    # Pause logic
    tool_context.request_confirmation(
        hint=f"Approving change: {original_task} -> {suggested_replacement}"
    )
    return {"status": "PENDING_APPROVAL"}

async def auto_save_to_memory(callback_context):
    """Saves session state to long-term memory."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

# ==========================================
# 3. AGENT DEFINITIONS
# ==========================================

# Define the Brain (Use the Lite model for tool compatibility)
llm_brain = Gemini(
    model="models/gemini-2.5-flash-lite", 
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# --- Rules Agent (Sub-Agent) ---
rules_agent = LlmAgent(
    name="RulesAgent",
    model=llm_brain,
    instruction="""You are the Formula Student Rules Lawyer.
    Your ONLY job is to check if a task complies with the 2026 Rules.
    1. Call `get_rules_from_db(category)` to get the official rules.
    2. Compare the task description against the rules.
    3. Return a JSON object with:
       - "compliant": true or false
       - "reason": "Quote the specific rule that was violated or satisfied."
    """,
    tools=[FunctionTool(func=get_rules_from_db)]
)

# --- Strategy Agent (Sub-Agent) ---
strategy_agent = LlmAgent(
    name="StrategyAgent",
    model=llm_brain,
    instruction="""You are an innovative Formula Student Chief Engineer.
    Your goal is to find creative solutions to engineering problems.
    
    You will receive a message describing a task that failed compliance.
    Your Process:
    1. Acknowledge the failure.
    2. Think of a new, alternative solution that achieves the same goal but follows the rules.
    3. Output your suggestion.
    """
)

# --- Team Manager Agent (The Boss) ---
team_manager_agent = LlmAgent(
    name="TeamManagerAgent",
    model=llm_brain,
    instruction="""You are the Formula Student Team Manager.
    
    Follow this STRICT process for every new task from the user:

    Step 1: Ask `RulesAgent` to check compliance.
    Step 2: ANALYZE the result.
       - IF compliant: Call `add_team_task` immediately.
       - IF NOT compliant: Proceed to Step 3.
    Step 3: Ask `StrategyAgent` for a fix.
       - Tell it the task failed and the reason.
    Step 4: Use `confirm_suggestion` to ask the user for approval.
       - Pass the 'original_task', 'suggested_replacement', and 'reason'.
    Step 5: FINALIZE.
       - If the tool returns "APPROVED", call `add_team_task` with the NEW suggestion.
       - If "REJECTED", stop.
    """,
    tools=[
        FunctionTool(func=add_team_task),
        FunctionTool(func=view_team_tasks),
        FunctionTool(func=confirm_suggestion),
        preload_memory
    ],
    sub_agents=[rules_agent, strategy_agent],
    after_agent_callback=auto_save_to_memory
)

# ==========================================
# 4. APP CONFIGURATION
# ==========================================

app = App(
    name="formula_student_copilot",
    root_agent=team_manager_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
