from game_sdk.game.agent import Agent, WorkerConfig
from game_sdk.game.custom_types import Function, Argument, FunctionResult, FunctionResultStatus
from typing import Tuple
import os
from dotenv import load_dotenv
import json

load_dotenv()

game_api_key = os.environ.get("GAME_API_KEY")

GHOST_PERFORMER_WORKER_ID = "ghost_performer"
SOUND_FX_OPERATOR_WORKER_ID = "sound_fx_operator"
FOG_MACHINE_TECH_WORKER_ID = "fog_machine_tech"

# ---- Logging Utility ----
def log_state_change(title: str, state: dict):
    print("\n" + "═" * 60)
    print(f"📦  STATE UPDATE → {title.upper()}".center(60))
    print("═" * 60)
    for key, value in state.items():
        print(f"   • {key:<18} → {value}")
    print("═" * 60 + "\n")


init_state = {
    "agent_state": {
        "scare_score": 0,
        "guest_stress_level": 0,
    },
    "worker_states": {
        GHOST_PERFORMER_WORKER_ID: {
            "prop_battery": 100,
            "ghost_placement": "unknown",
        },
        SOUND_FX_OPERATOR_WORKER_ID: {
            "speaker_battery": 100
        },
        FOG_MACHINE_TECH_WORKER_ID: {
            "fog_fluid_level": 100
        }
    }
}

# ----- Worker State Management -----
def get_ghost_performer_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    print(f"Using get ghost performer worker state -> current state: {current_state}")

    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    if function_result is not None:
        info = function_result.info
        print("\n" + "-" * 60)
        print(f"🔧 GHOST PERFORMER WORKER UPDATE ({info.get('action', '').upper()})".center(60))
        print("-" * 60)
        print("📤 Action Info:")
        print(json.dumps(info, indent=4))

        action = info.get("action", None)

        if action and function_result.action_status == FunctionResultStatus.DONE and current_state.get("worker_states", {}).get(GHOST_PERFORMER_WORKER_ID, {}).get("prop_battery", 0) > 0:
            current_state["worker_states"][GHOST_PERFORMER_WORKER_ID]["prop_battery"] -= 10
            print(f"   🔋 prop_battery decreased to {current_state["worker_states"][GHOST_PERFORMER_WORKER_ID]["prop_battery"]}")

            if action == "move_ghost":
                location = info.get("location", "unknown")
                current_state["worker_states"][GHOST_PERFORMER_WORKER_ID]["ghost_placement"] = location
                print(f"   👻 ghost_placement updated to {location}")


    log_state_change("Updated Worker State", current_state["worker_states"][GHOST_PERFORMER_WORKER_ID])
    return current_state

def get_sound_fx_operator_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    print(f"Using get sound fx operator worker state -> current state: {current_state}")

    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    if function_result is not None:
        info = function_result.info
        print("\n" + "-" * 60)
        print(f"🔧 SOUND FX OPERATOR WORKER UPDATE ({info.get('action', '').upper()})".center(60))
        print("-" * 60)
        print("📤 Action Info:")
        print(json.dumps(info, indent=4))
    
    action = info.get("action", None)

    if action and function_result.action_status == FunctionResultStatus.DONE and current_state.get("worker_states", {}).get(SOUND_FX_OPERATOR_WORKER_ID, {}).get("speaker_battery", 0) > 0:
        current_state["worker_states"][SOUND_FX_OPERATOR_WORKER_ID]["speaker_battery"] -= 10
        print(f"   🔋 speaker_battery decreased to {current_state["worker_states"][SOUND_FX_OPERATOR_WORKER_ID]["speaker_battery"]}")

    log_state_change("Updated Worker State", current_state["worker_states"][SOUND_FX_OPERATOR_WORKER_ID])
    return current_state


def get_fog_machine_tech_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    print(f"Using get sound fx operator worker state -> current state: {current_state}")

    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    if function_result is not None:
        info = function_result.info
        print("\n" + "-" * 60)
        print(f"😶‍🌫️ FOG MACHINE TECH WORKER UPDATE ({info.get('action', '').upper()})".center(60))
        print("-" * 60)
        print("📤 Action Info:")
        print(json.dumps(info, indent=4))
        
    action = info.get("action", None)

    if action and function_result.action_status == FunctionResultStatus.DONE and current_state.get("worker_states", {}).get(FOG_MACHINE_TECH_WORKER_ID, {}).get("fog_fluid_level", 0) > 0:
        current_state["worker_states"][FOG_MACHINE_TECH_WORKER_ID]["fog_fluid_level"] -= 10
        print(f"   💧 fog_fluid_level decreased to {current_state["worker_states"][FOG_MACHINE_TECH_WORKER_ID]["fog_fluid_level"]}")

    log_state_change("Updated Worker State", current_state["worker_states"][FOG_MACHINE_TECH_WORKER_ID])
    return current_state

# ----- Agent State Management -----
def get_agent_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    print(f"Using get agent state -> current state: {current_state}")

    if current_state is None:
        print("[AGENT STATE INIT] Initialized new agent state...")
        return init_state

    if function_result is not None:
        info = function_result.info
        print("\n" + "=" * 60)
        print(f"🧠 AGENT UPDATE ({info.get('action', '').upper()})".center(60))
        print("=" * 60)
        print("📤 Action Info:")
        print(json.dumps(info, indent=4))

        if info.get("action") == "scare_guest":
            scare_pts = info.get("scare_points", 0)
            stress_pts = info.get("stress_points", 0)
            current_state["agent_state"]["scare_score"] += scare_pts
            current_state["agent_state"]["guest_stress_level"] += stress_pts
            print(f"   🎯 scare_score +{scare_pts} → {current_state["agent_state"]["scare_score"]}")
            print(f"   😱 guest_stress_level +{stress_pts} → {current_state["agent_state"]["guest_stress_level"]}")

    log_state_change("Updated Agent State", current_state["agent_state"])
    return current_state

# ----- Worker Functions -----
def move_ghost(location: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n[move_ghost] ➡️ Moving ghost to {location}")
    return FunctionResultStatus.DONE, f"Ghost moved to {location}!", {"action": "move_ghost", "location": location}

def trigger_sound_fx(effect: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n[trigger_sound_fx] 🔊 Triggering sound effect: {effect}")
    return FunctionResultStatus.DONE, f"Sound effect '{effect}' triggered!", {"action": "scare_guest", "scare_points": 3, "stress_points": 2}

def trigger_fog_machine(**kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n[trigger_fog_machine] 🌫️ Activating fog machine.")
    return FunctionResultStatus.DONE, "Fog machine activated!", {"action": "trigger_prop"}

# ----- Function Declarations -----
move_ghost_fn = Function(
    fn_name="move_ghost",
    fn_description="Move the ghost to a new location",
    args=[Argument(name="location", type="string", description="Location to move the ghost to")],
    executable=move_ghost
)

trigger_sound_fx_fn = Function(
    fn_name="trigger_sound_fx",
    fn_description="Trigger a spooky sound effect",
    args=[Argument(name="effect", type="string", description="Type of sound effect to play")],
    executable=trigger_sound_fx
)

trigger_fog_fn = Function(
    fn_name="trigger_fog",
    fn_description="Trigger the fog machine",
    args=[],
    executable=trigger_fog_machine
)

# ----- Workers -----
ghost_performer = WorkerConfig(
    id=GHOST_PERFORMER_WORKER_ID,
    worker_description="Responsible for scaring guests by appearing suddenly.",
    get_state_fn=get_ghost_performer_worker_state_fn,
    action_space=[move_ghost_fn]
)

sound_fx_operator = WorkerConfig(
    id=SOUND_FX_OPERATOR_WORKER_ID,
    worker_description="Handles sound effects to increase the scare factor.",
    get_state_fn=get_sound_fx_operator_worker_state_fn,
    action_space=[trigger_sound_fx_fn]
)

fog_machine_tech = WorkerConfig(
    id=FOG_MACHINE_TECH_WORKER_ID,
    worker_description="Operates the fog machine to set the mood.",
    get_state_fn=get_fog_machine_tech_worker_state_fn,
    action_space=[trigger_fog_fn]
)

# ----- Haunted House Agent -----
haunted_agent = Agent(
    api_key=game_api_key,
    name="Haunted House Manager",
    agent_goal="Maximize guest screams and stress by strategically coordinating different haunted house props in each round. Ensure a balanced use of ghost performer, sound effects, and fog machine to create a layered and immersive scare experience.",
    agent_description="You are the mastermind behind a haunted house attraction. Time every scare perfectly.",
    get_agent_state_fn=get_agent_state_fn,
    workers=[ghost_performer, sound_fx_operator, fog_machine_tech],
    model_name="Llama-3.1-405B-Instruct"
)

# ----- Compile and Run -----
print("\n🎬 Launching Haunted House Simulation...\n")
haunted_agent.compile()
haunted_agent.run()
