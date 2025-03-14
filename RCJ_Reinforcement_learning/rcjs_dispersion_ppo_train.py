import os

from sb3_contrib import RecurrentPPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from RCJ_Reinforcement_learning.environment.rcjs_first_environment import FirstEnvironment
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback


checkpoint_callback = CheckpointCallback(save_freq=100000,
                                         save_path='model',
                                         name_prefix='RCJ_ppo_model',
                                         save_replay_buffer=True,
                                         save_vecnormalize=True)

def make_env():
    def _init():
        env = FirstEnvironment(max_steps=10000,
                               create_position=[0, 0, 0],
                               magnitude=10.0,
                               gui=False)
        check_env(env)
        return env
    return _init

def main():
    save_dir = "model"
    os.makedirs(save_dir, exist_ok=True)

    num_envs = 12
    env = SubprocVecEnv([make_env() for _ in range(num_envs)])

    model = RecurrentPPO("MlpLstmPolicy",
                env,
                device="cuda",
                verbose=1,
                n_epochs=10,
                n_steps=128,
                batch_size=128*12,
                gamma=0.99)

    model.learn(total_timesteps=100000000, callback=checkpoint_callback)
    model.save(os.path.join(save_dir, "RCJ_ppo_model_v2"))

    env.close()

if __name__ == "__main__":
    main()





