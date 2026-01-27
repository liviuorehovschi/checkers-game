# Checkers Game

A web-based checkers game with an AI opponent using minimax algorithm with alpha-beta pruning.

## Features

- **Play vs Computer**: Challenge an AI opponent that uses strategic decision-making
- **Play vs Human**: Two players can take turns on the same device
- **Smooth Animations**: AI moves are animated for better visual feedback
- **Turn Indicator**: Clear display of whose turn it is
- **Mandatory Captures**: Enforces the rule that captures must be made when available

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **AI**: Minimax algorithm with alpha-beta pruning

## Local Setup

### Prerequisites

- Python 3.6 or later
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/liviuorehovschi/checkers-game.git
cd checkers-game
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```

5. Open http://localhost:5000 in your browser

## Running Tests

```bash
python test.py
```

## Deployment

This app is configured for Vercel deployment. Simply connect your GitHub repo to Vercel and it will deploy automatically.
