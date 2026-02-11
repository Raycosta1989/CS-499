import numpy as np
import random
import datetime


class TrainingConfig:
    """Configuration for Q-learning training."""

    def __init__(
        self,
        n_epoch=15000,
        max_memory=1000,
        batch_size=16,
        train_epochs=4,
        epsilon_start=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        win_rate_threshold=0.9,
    ):
        self.n_epoch = n_epoch
        self.max_memory = max_memory
        self.batch_size = batch_size
        self.train_epochs = train_epochs
        self.epsilon_start = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.win_rate_threshold = win_rate_threshold


class QLearningAgent:
    """Q-learning agent that selects actions using an epsilon-greedy policy."""

    def __init__(self, model, experience, config: TrainingConfig):
        self.model = model
        self.experience = experience
        self.config = config
        self.epsilon = config.epsilon_start

    def select_action(self, state, valid_actions):
        """Select an action using epsilon-greedy strategy."""
        if not valid_actions:
            return None

        # Exploration vs exploitation
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            q_values = self.experience.predict(state)
            return int(np.argmax(q_values))

    def decay_epsilon(self):
        """Decay epsilon but never below minimum."""
        self.epsilon = max(self.config.epsilon_min, self.epsilon * self.config.epsilon_decay)


class QTrainer:
    """Trainer that coordinates environment, agent, and learning loop."""

    def __init__(self, model, maze, experience, config: TrainingConfig):
        self.model = model
        self.maze = TreasureMaze(maze)
        self.experience = experience
        self.config = config
        self.agent = QLearningAgent(model, experience, config)

    def train(self):
        start_time = datetime.datetime.now()
        win_history = []
        hsize = self.maze.maze.size // 2

        for epoch in range(self.config.n_epoch):
            agent_cell = random.choice(self.maze.free_cells)
            self.maze.reset(agent_cell)
            state = self.maze.observe()

            game_over = False
            n_episodes = 0
            loss = 0.0
            win_rate = 0.0

            while not game_over:
                prev_state = state
                valid_actions = self.maze.valid_actions()

                if not valid_actions:
                    break

                action = self.agent.select_action(prev_state, valid_actions)
                state, reward, status = self.maze.act(action)

                episode = [prev_state, action, reward, state, status]
                self.experience.remember(episode)

                inputs, targets = self.experience.get_data()
                self.model.fit(
                    inputs,
                    targets,
                    epochs=self.config.train_epochs,
                    batch_size=self.config.batch_size,
                    verbose=0,
                )
                loss = self.model.evaluate(inputs, targets, verbose=0)
                n_episodes += 1

                if status == "win":
                    win_history.append(1)
                    game_over = True
                elif status == "lose":
                    win_history.append(0)
                    game_over = True

                if len(win_history) > 0:
                    win_rate = sum(win_history[-hsize:]) / hsize

            self.agent.decay_epsilon()

            dt = datetime.datetime.now() - start_time
            t = format_time(dt.total_seconds())
            print(
                f"Epoch: {epoch:03d}/{self.config.n_epoch - 1} | "
                f"Loss: {loss:.4f} | Episodes: {n_episodes} | "
                f"Win count: {sum(win_history)} | Win rate: {win_rate:.3f} | time: {t}"
            )

            if win_rate >= self.config.win_rate_threshold and completion_check(self.model, self.maze):
                print(f"Reached target win rate at epoch: {epoch}")
                break

        total_time = datetime.datetime.now() - start_time
        seconds = total_time.total_seconds()
        print(
            f"n_epoch: {epoch}, max_mem: {self.config.max_memory}, "
            f"batch_size: {self.config.batch_size}, time: {format_time(seconds)}"
        )
        return seconds


def format_time(seconds):
    if seconds < 400:
        return f"{seconds:.1f} seconds"
    elif seconds < 4000:
        return f"{seconds / 60.0:.2f} minutes"
    else:
        return f"{seconds / 3600.0:.2f} hours"
