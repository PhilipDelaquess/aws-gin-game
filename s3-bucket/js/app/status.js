define(function (require) {
  "use strict";

  var React = require('react');

  var Status = React.createClass({
    render: function () {
      var stateMsg = '';
      if (this.props.state == 'AWAITING_OPPONENT_ACTION') {
        if (this.props.opponentState == 'PONE_INITIAL_DRAW') {
          stateMsg = 'You dealt. Waiting for ' + this.props.opponentName + ' to take the initial discard.';
        } else if (this.props.opponentState == 'DEALER_INITIAL_DRAW') {
          stateMsg = 'Waiting for ' + this.props.opponentName + ' to take the initial discard.';
        } else if (this.props.opponentState == 'NORMAL_DRAW') {
          stateMsg = 'Waiting for ' + this.props.opponentName + ' to draw.';
        } else if (this.props.opponentState == 'DISCARD_OR_KNOCK') {
          if (this.props.opponentLastDraw) {
            stateMsg = this.props.opponentName + ' drew from the discard pile ';
          } else {
            stateMsg = this.props.opponentName + ' drew from the deck ';
          }
          stateMsg += 'and needs to discard.';
        } else if (this.props.opponentState == 'ACKNOWLEDGE_DEAL') {
          stateMsg = 'Waiting for ' + this.props.opponentName + ' to OK the last deal';
        }
      } else if (this.props.state == 'PONE_INITIAL_DRAW') {
        stateMsg = this.props.opponentName + ' dealt, and awaits your decision.';
      } else if (this.props.state == 'DEALER_INITIAL_DRAW') {
        stateMsg = this.props.opponentName + ' declined the initial discard.';
      } else if (this.props.state == 'NORMAL_DRAW') {
        stateMsg = 'Your turn. Draw from the deck or the discard pile.';
      } else if (this.props.state == 'DISCARD_OR_KNOCK') {
        stateMsg = 'Your turn. Click the card you want to discard.';
      }
      return React.DOM.h3({}, stateMsg);
    }
  });

  return React.createFactory(Status);
});
