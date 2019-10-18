var board = null
var game = new Chess()

/*$('#startPositionBtn').on('click', () => {
    if (board != null){board.start; return;}
)*/


$('#startPositionBtn').on('click', () => {
 game = new Chess();
 board.position(game.fen())
    document.getElementById('msg').innerHTML=""
    document.getElementById('info').innerHTML=""
    document.getElementById('img').setAttribute('src', "")
})

function onDragStart (source, piece, position, orientation) {

  if (game.game_over()) return false

  if (piece.search(/^b/) !== -1) return false
}

function getLegalMoves () {
    const moves = game.moves({'verbose': true})
    var formatted_moves = []

    moves.forEach(move => formatted_moves.push(move.from + move.to))
    return formatted_moves
}

function makeComputerMove () {

  var fen_board = game.fen()
  var bestMove;

  $.post( "game", {
                    'position': fen_board
                  })
    .done(function( data ) {
        if (data.hasOwnProperty("msg")){
            document.getElementById('msg').innerHTML=data.msg
        }else{
            document.getElementById('msg').innerHTML=""
        }
        if (data.hasOwnProperty("info")){
            document.getElementById('info').innerHTML=data.info
        }else{
            document.getElementById('info').innerHTML=""
        }
        if (data.hasOwnProperty("img")){
            document.getElementById('img').setAttribute('src', data.img)
        }else{
            document.getElementById('img').setAttribute('src', "")
        }
        if (data.hasOwnProperty("resetBoard")) {
            game = new Chess()
            board.position(game.fen())
        }else {
            bestMove = data.bestMove
            game.move({from: bestMove.substring(0, 2), to: bestMove.substring(2, 4)});
            board.position(game.fen())
        }
  });

}

function onDrop (source, target) {

  var legalMoves = getLegalMoves()

    var move = game.move({
    from: source,
    to: target,
    promotion: 'q'
    })

    if (move === null) return 'snapback'

    const moveIsIllegal = legalMoves.includes(move.from + move.to) == false

  if (moveIsIllegal) {
      return 'snapback'
  }



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