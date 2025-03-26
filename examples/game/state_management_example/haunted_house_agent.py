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


def log_action_info(action: str, info: dict):
    print("\n" + "-" * 60)
    print(f"🔧 {action.upper()} WORKER UPDATE".center(60))
    print("-" * 60)
    print("📤 Action Info:")
    print(json.dumps(info, indent=4))


# ---- Shared Worker State Update ----
def update_worker_state(worker_id: str, function_result: FunctionResult, current_state: dict, updates: dict):
    if function_result is not None:
        info = function_result.info
        log_action_info(worker_id, info)

        if function_result.action_status == FunctionResultStatus.DONE:
            worker_state = current_state["worker_states"][worker_id]

            for key, change in updates.items():
                if key in worker_state:
                    worker_state[key] = max(0, worker_state[key] + change)

            log_state_change(f"Updated Worker State ({worker_id})", worker_state)

    return current_state


# ---- Initial State ----
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


# ----- Worker State Functions -----
def get_ghost_performer_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    if function_result and function_result.info.get("action") == "move_ghost":
        location = function_result.info.get("location", "unknown")
        current_state["worker_states"][GHOST_PERFORMER_WORKER_ID]["ghost_placement"] = location

    return update_worker_state(
        GHOST_PERFORMER_WORKER_ID,
        function_result,
        current_state,
        updates={"prop_battery": -10}
    )


def get_sound_fx_operator_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    return update_worker_state(
        SOUND_FX_OPERATOR_WORKER_ID,
        function_result,
        current_state,
        updates={"speaker_battery": -10}
    )


def get_fog_machine_tech_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    if current_state is None:
        print("[WORKER STATE INIT] Initialized new worker state.")
        return init_state

    return update_worker_state(
        FOG_MACHINE_TECH_WORKER_ID,
        function_result,
        current_state,
        updates={"fog_fluid_level": -10}
    )


# ----- Agent State Management -----
def get_agent_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    print(f"\n\n 🎃🎃🎃 Using get agent state → current state: {current_state}🎃🎃🎃")

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
            print(f"\n   🎯 scare_score +{scare_pts} → {current_state['agent_state']['scare_score']}")
            print(f"   😱 guest_stress_level +{stress_pts} → {current_state['agent_state']['guest_stress_level']}\n")

    log_state_change("Updated Agent State", current_state["agent_state"])
    return current_state


# ----- Worker Functions -----
def move_ghost(location: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n\n🎃 [move_ghost] ➡️ Moving ghost to '{location}' 🎃\n")
    return FunctionResultStatus.DONE, f"Ghost moved to {location}!", {
        "action": "move_ghost",
        "location": location
    }


def trigger_sound_fx(effect: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n\n🔊 [trigger_sound_fx] Triggering sound effect: '{effect}' 🔊\n")
    return FunctionResultStatus.DONE, f"Sound effect '{effect}' triggered!", {
        "action": "scare_guest",
        "scare_points": 3,
        "stress_points": 2,
        "effect": effect
    }


def trigger_fog_machine(**kwargs) -> Tuple[FunctionResultStatus, str, dict]:
    print(f"\n\n🌫️ [trigger_fog_machine] Activating fog machine 🌫️\n")
    return FunctionResultStatus.DONE, "Fog machine activated!", {
        "action": "fog_fluid_level" 
    }


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
    agent_description="You are the mastermind behind a haunted house attraction. In every round, orchestrate a perfectly timed scare using a mix of ghost, sound, and fog. Don't repeat the same prop twice in a row.",
    get_agent_state_fn=get_agent_state_fn,
    workers=[ghost_performer, sound_fx_operator, fog_machine_tech],
    model_name="Llama-3.1-405B-Instruct"
)


# ----- Compile and Run -----
print("\n🎬 Launching Haunted House Simulation...\n")
haunted_agent.compile()
haunted_agent.run()