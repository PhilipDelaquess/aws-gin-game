define(function (require) {
  "use strict";
  var React = require('react'),
    Melding = require('app/melding');

  var Score = React.createClass({
    okClicked: function () {
      this.props.callback();
    },

    render: function () {
      var player = this.props.player;
      var playerKnocked = player.summary.knockerId == player.id;
      var knockName = playerKnocked ? 'You' : player.opponentName;
      var otherName = playerKnocked ? player.opponentName : 'You';
      var scoreName = (playerKnocked  != player.summary.undercut) ? 'You' : player.opponentName;
      var stmt = scoreName + ' gained ' + player.summary.score + ' points';
      if (player.summary.gin) {
        stmt += ' with GIN!';
      } else if (player.summary.undercut) {
        stmt += ' by UNDERCUT!';
      }
      var gameOverMessage = player.score >= 100 || player.opponentScore >= 100
        ? scoreName + ' WON!' : '';
      return React.DOM.div({},
        React.DOM.h1({},
          React.DOM.span({className: 'blue'}, player.name + ': '),
          React.DOM.span({className: 'gray'}, player.score),
          React.DOM.span({className: 'blue'}, ' vs ' + player.opponentName + ': '),
          React.DOM.span({className: 'gray'}, player.opponentScore)
        ),
        React.DOM.h3({}, knockName + ' knocked with'),
        Melding({melding: player.summary.knockerMelding}),
        React.DOM.h3({}, otherName + ' had'),
        Melding({melding: player.summary.otherMelding}),
        React.DOM.h3({}, stmt),
        React.DOM.h1({className: 'red'}, gameOverMessage),
        React.DOM.h1({},
          React.DOM.span({
            onClick: this.okClicked,
            className: 'card blue'
          }, 'OK')
        )
      );
    }
  });

  return React.createFactory(Score);
});
