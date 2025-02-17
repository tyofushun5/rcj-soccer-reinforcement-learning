import os

from stable_baselines3 import PPO

from RCJ_Reinforcement_learning.environment.rcjs_first_environment import Environment


save_dir = "model"
os.makedirs(save_dir, exist_ok=True)

def main():
    env = Environment(max_steps=15000,
                      create_position=[0, 0, 0],
                      gui=True)

    model = PPO("MlpPolicy",
                env,
                device="cpu",
                verbose=1,
                n_epochs=10,
                n_steps=4096,
                batch_size=4096,
                gamma=0.99)

    model.learn(total_timesteps=5000000)

    model.save(os.path.join(save_dir, "RCJ_ppo_model_v1"))

    env.close()

if __name__ == "__main__":
    main()
