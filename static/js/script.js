document.addEventListener("DOMContentLoaded", function() {
    let selectedPiece = null;
    let currentPlayer = 'R';
    let gameMode = localStorage.getItem('gameMode') || 'ai';
    let isAnimating = false;

    // Initialize mode buttons
    updateModeButtons();

    document.getElementById("board").addEventListener("click", function(event) {
        // Prevent moves during animation or during CPU's turn in AI mode
        if (isAnimating) return;
        if (gameMode === 'ai' && currentPlayer !== 'R') return;

        let clickedElement = event.target;

        // Check if clicked on a piece belonging to current player
        if (clickedElement.classList.contains("piece") &&
            (clickedElement.classList.contains(currentPlayer) ||
             clickedElement.classList.contains(`${currentPlayer}Q`))) {

            // Deselect previous piece
            if (selectedPiece) {
                selectedPiece.classList.remove('selected');
            }

            selectedPiece = clickedElement;
            selectedPiece.classList.add('selected');

        } else if (selectedPiece && clickedElement.classList.contains("cell")) {
            let startX = parseInt(selectedPiece.parentElement.dataset.x, 10);
            let startY = parseInt(selectedPiece.parentElement.dataset.y, 10);
            let endX = parseInt(clickedElement.dataset.x, 10);
            let endY = parseInt(clickedElement.dataset.y, 10);

            fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ start: [startX, startY], end: [endX, endY] }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    // Clear selection
                    if (selectedPiece) {
                        selectedPiece.classList.remove('selected');
                    }
                    selectedPiece = null;

                    // Check if there are CPU moves to animate
                    if (data.cpu_moves && data.cpu_moves.length > 0) {
                        // First update board to show player's move result (before CPU)
                        // We need intermediate board state, but API gives us final state
                        // So we'll animate CPU moves on top of final state
                        updateBoardWithoutCpuPieces(data.board, data.cpu_moves);
                        animateCpuMoves(data.cpu_moves, data.board, () => {
                            currentPlayer = data.current_player;
                            updateTurnIndicator();
                            if (data.game_over) {
                                setTimeout(() => {
                                    let message = `Game Over. ${data.winner === 'R' ? 'Red' : 'Black'} wins!`;
                                    alert(message);
                                }, 100);
                            }
                        });
                    } else {
                        updateBoard(data.board);
                        currentPlayer = data.current_player;
                        updateTurnIndicator();

                        if (data.game_over) {
                            let message = `Game Over. ${data.winner === 'R' ? 'Red' : 'Black'} wins!`;
                            alert(message);
                        }
                    }
                } else if (data.mandatory_capture) {
                    alert("A capture is available and mandatory. You must make a capture move.");
                }
            });
        }
    });

    function updateBoardWithoutCpuPieces(finalBoard, cpuMoves) {
        // For animation, we show the board state before CPU moves started
        // by placing CPU pieces at their original positions
        let boardCopy = JSON.parse(JSON.stringify(finalBoard));

        // Work backwards through CPU moves to find original positions
        let piecePositions = [];
        for (let i = cpuMoves.length - 1; i >= 0; i--) {
            let move = cpuMoves[i];
            if (i === cpuMoves.length - 1) {
                // Last move: piece is at end position in final board
                piecePositions.unshift({ move: move, piece: boardCopy[move.end[0]][move.end[1]] });
                boardCopy[move.end[0]][move.end[1]] = ' ';
            } else {
                // Earlier moves
                piecePositions.unshift({ move: move, piece: piecePositions[0].piece });
            }
        }

        // Place piece at first move's start position
        if (cpuMoves.length > 0) {
            boardCopy[cpuMoves[0].start[0]][cpuMoves[0].start[1]] = piecePositions[0].piece;
        }

        updateBoard(boardCopy);
    }

    function animateCpuMoves(moves, finalBoard, callback) {
        if (moves.length === 0) {
            callback();
            return;
        }

        isAnimating = true;
        let moveIndex = 0;

        function animateNextMove() {
            if (moveIndex >= moves.length) {
                isAnimating = false;
                updateBoard(finalBoard);
                callback();
                return;
            }

            let move = moves[moveIndex];
            let startCell = document.querySelector(`.cell[data-x="${move.start[0]}"][data-y="${move.start[1]}"]`);
            let endCell = document.querySelector(`.cell[data-x="${move.end[0]}"][data-y="${move.end[1]}"]`);
            let piece = startCell.querySelector('.piece');

            if (!piece) {
                moveIndex++;
                animateNextMove();
                return;
            }

            // Calculate the translation
            let startRect = startCell.getBoundingClientRect();
            let endRect = endCell.getBoundingClientRect();
            let deltaX = endRect.left - startRect.left;
            let deltaY = endRect.top - startRect.top;

            // Add animating class and apply transform
            piece.classList.add('animating');
            piece.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

            // After animation completes
            setTimeout(() => {
                piece.classList.remove('animating');
                piece.style.transform = '';

                // Move piece to new cell in DOM
                startCell.innerHTML = '';
                endCell.innerHTML = '';

                // Check if this is the last move to get final piece state
                if (moveIndex === moves.length - 1) {
                    // Use final board state for this piece
                    let finalPieceClass = finalBoard[move.end[0]][move.end[1]];
                    let className = 'piece ' + finalPieceClass;
                    if (finalPieceClass.includes('Q')) {
                        className += ' queen';
                    }
                    endCell.innerHTML = `<div class="${className}"></div>`;
                } else {
                    // Keep current piece class for intermediate moves
                    let pieceClasses = piece.className.replace('animating', '').trim();
                    endCell.innerHTML = `<div class="${pieceClasses}"></div>`;
                }

                // Handle capture - remove captured piece
                if (Math.abs(move.start[0] - move.end[0]) === 2) {
                    let midRow = Math.floor((move.start[0] + move.end[0]) / 2);
                    let midCol = Math.floor((move.start[1] + move.end[1]) / 2);
                    let midCell = document.querySelector(`.cell[data-x="${midRow}"][data-y="${midCol}"]`);
                    if (midCell) {
                        midCell.innerHTML = '';
                    }
                }

                moveIndex++;
                // Small delay between multi-captures
                setTimeout(animateNextMove, 150);
            }, 400);
        }

        // Start with a small delay so player sees their move first
        setTimeout(animateNextMove, 300);
    }

    function updateBoard(newBoard) {
        let cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            let row = Math.floor(index / 8);
            let col = index % 8;
            let pieceType = newBoard[row][col];

            if (pieceType === ' ') {
                cell.innerHTML = '';
            } else {
                let className = 'piece ' + pieceType;
                if (pieceType.includes('Q')) {
                    className += ' queen';
                }
                cell.innerHTML = `<div class="${className}"></div>`;
            }
        });
    }

    function updateTurnIndicator() {
        let indicator = document.getElementById('turn-indicator');
        if (currentPlayer === 'R') {
            indicator.textContent = "Red's Turn";
            indicator.className = 'turn-indicator red-turn';
        } else {
            indicator.textContent = "Black's Turn";
            indicator.className = 'turn-indicator black-turn';
        }
    }

    function updateModeButtons() {
        document.getElementById('mode-ai').classList.toggle('active', gameMode === 'ai');
        document.getElementById('mode-human').classList.toggle('active', gameMode === 'human');
    }

    window.setMode = function(mode) {
        if (mode === gameMode) return;

        gameMode = mode;
        localStorage.setItem('gameMode', mode);
        updateModeButtons();

        // Reset game with new mode
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mode: mode }),
        }).then(() => {
            window.location.reload();
        });
    };

    window.resetGame = function() {
        localStorage.removeItem('gameMode');
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mode: gameMode }),
        }).then(() => {
            window.location.reload();
        });
    };
});
