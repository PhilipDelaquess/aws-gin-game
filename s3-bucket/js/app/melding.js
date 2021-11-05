define(function (require) {
  "use strict";
  var React = require('react'),
    Card = require('app/card').Card;

  var Melding = React.createClass({
    getInitialState: function () {
      return {
        isPrompting: false,
        pendingAbbrev: null
      }
    },

    clickedCard: function (abbrev) {
      if (this.props.callback) {
        if (_.contains(this.props.melding.knockables, abbrev)) {
          this.setState({isPrompting: true, pendingAbbrev: abbrev});
        } else {
          this.props.callback(abbrev, false);
        }
      }
    },

    discardPending: function (e) {
      var knock = e.target.id == 'knock';
      this.props.callback(this.state.pendingAbbrev, knock);
      this.setState({isPrompting: false, pendingAbbrev: null});
    },

    renderMeld: function (meld) {
      var spans = _.map(meld.cards, function (card) {
        return Card({
          key: card,
          callback: this.state.isPrompting || !this.props.callback ? null : this.clickedCard,
          card: card,
          lastDraw: this.props.lastDraw
        });
      }.bind(this));
      return React.DOM.span({key: meld.key, className: 'meld'}, spans);
    },

    render: function () {
      var spans = _.map(this.props.melding.melds, function (meld) {
        return this.renderMeld(meld);
      }.bind(this));
      _.each(this.props.melding.deadwood, function (card) {
        spans.push(Card({
          key: card,
          callback: this.state.isPrompting || !this.props.callback ? null : this.clickedCard,
          card: card,
          lastDraw: this.props.lastDraw
        }));
      }, this);
      if (this.state.isPrompting) {
        spans.push(React.DOM.span({key: 'prompts'},
          React.DOM.span({
            className: 'card blue',
            onClick: this.discardPending,
            id: 'knock'
          }, 'Knock'),
          React.DOM.span({
            className: 'card blue',
            onClick: this.discardPending
          }, 'Discard')
        ))
      }
      spans.push(React.DOM.span({key: 'score', className: 'gray'}, ' ' + this.props.melding.score));
      return React.DOM.h1({className: 'melding'}, spans);
    }
  });

  return React.createFactory(Melding);
});
