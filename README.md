
# Alfred 🎩

Alfred is a super flexible automation tool designed to simplify your workflows. Use it to orchestrate tasks, manage steps in a process and distribute the workload! 🚀

## What does it do? 🤔

- Executes a series of *steps* in sequence.
- Logs everything that happens (because we never want to lose track!).
- Fully customizable to fit whatever you need to do. 😎

## Key Features 🔥

- **Flexible design**: Use your favorite programming language to automate your CI process, leverage your knowledge to build complex pipelines
- **Full logging**: Every step gets recorded to track what happened.
- **Automate everything**: Run complex tasks easily and linearly.
- **Integration support**: Use pre-built blocks to connect Alfred to Git, Slack, and other tools to extend functionality. 

## How to use it? 🚀

1. Clone the repo:

```bash
git clone https://github.com/simone-gheller/alfred.git
cd alfred
```

2. Install dependencies (make sure you have Python and `pip`):

```bash
pip install -r requirements.txt
```

3. Create your own pipeline by defining steps and executing them:

```python
from api.alfred import *

# Define your steps
def step1(): return "hello world"
def step2(data): return data.upper()

# Create pipeline
pipeline = Pipeline([
    Step(step1),
    Step(step2)]
)

# Run it!
run_pipeline()
```

## Contributing 🤝

Feel free to fork and contribute! Open an issue if you find a bug or want to suggest a feature. Pull requests are welcome!

## License 📄

Distributed under the MIT License. See `LICENSE` for more information.
