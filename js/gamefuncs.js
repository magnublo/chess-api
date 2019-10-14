var board = null
var game = new Chess()

function onDragStart (source, piece, position, orientation) {

  if (game.game_over()) return false

  if (piece.search(/^b/) !== -1) return false
}

function makeComputerMove () {

  var fen_board = game.fen()
  var bestMove;

  $.post( "game", {
                    'position': fen_board
                  })
    .done(function( data ) {
      bestMove = data.bestMove
      console.log(bestMove.substring(2,4))
      game.move({ from: bestMove.substring(0,2), to: bestMove.substring(2,4) });
      board.position(game.fen())
  });

}

function onDrop (source, target) {

  var move = game.move({
    from: source,
    to: target,
    promotion: 'q'
  })

  if (move === null) return 'snapback'

  window.setTimeout(makeComputerMove, 250)
}

function onSnapEnd () {

}

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}