define(function (require) {
  "use strict";
  var React = require('react'),
    _ = require('underscore'),
    Hand = require('app/hand'),
    Card = require('app/card').Card,
    Status = require('app/status');

  var Game = React.createClass({

    clickedDeck: function () {
      if (this.props.deckCallback) {
        this.props.deckCallback();
      }
    },

    clickedReject: function () {
      this.props.rejectCallback();
    },

    renderDeck: function () {
      var className = 'card blue';
      if (!this.props.deckCallback) {
        className += ' disabled';
      }
      return React.DOM.h1({},
        React.DOM.span({},
          React.DOM.span({className: 'gray'}, 'Deck: '),
          React.DOM.span({
            className: className,
            onClick: this.clickedDeck
          }, this.props.player.packSize)
        )
      );
    },

    renderDiscard: function () {
      return React.DOM.h1({},
        React.DOM.span({},
          React.DOM.span({className: 'gray'}, 'Top Discard: '),
          Card({
            callback: this.props.wasteCallback,
            card: this.props.player.topDiscard
          }),
          this.props.rejectCallback
            ? React.DOM.span({
              className: 'card blue',
              onClick: this.clickedReject
            }, 'No thanks')
            : React.DOM.span({})
        )
      );
    },

    render: function () {
      return React.DOM.div({},
        React.DOM.h1({},
          React.DOM.span({className: 'blue'}, this.props.player.name + ': '),
          React.DOM.span({className: 'gray'}, this.props.player.score),
          React.DOM.span({className: 'blue'}, ' vs ' + this.props.player.opponentName + ': '),
          React.DOM.span({className: 'gray'}, this.props.player.opponentScore)
        ),
        this.renderDeck(),
        this.renderDiscard(),
        Hand({
          callback: this.props.cardCallback,
          hand: this.props.player.hand,
          lastDraw: this.props.player.lastDraw
        }),
        Status(_.pick(this.props.player, 'state', 'opponentState', 'opponentLastDraw', 'opponentName')));
    }
  });

  return React.createFactory(Game);
});