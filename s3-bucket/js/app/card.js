define(function (require) {
  "use strict";
  var React = require('react');

  var SuitMap = {
    'C': {clazz: 'black', unicode: '\u2663'},
    'D': {clazz: 'red', unicode: '\u2666'},
    'H': {clazz: 'red', unicode: '\u2665'},
    'S': {clazz: 'black', unicode: '\u2660'}
  };

  var Card = React.createClass({
    handleClick: function () {
      if (this.props.callback) {
        this.props.callback(this.props.card);
      }
    },

    render: function () {
      var clazz = 'card ' + (this.props.card ? SuitMap[this.props.card.slice(-1)].clazz : '');
      if (this.props.card && this.props.lastDraw == this.props.card) {
        clazz += ' last-draw';
      }
      if (!this.props.callback) {
        clazz += ' disabled';
      }
      var str = this.props.card ? SuitMap[this.props.card.slice(-1)].unicode + this.props.card.slice(0,-1) : '--';
      return React.DOM.span({
        onClick: this.handleClick,
        className: clazz
      }, str);
    }
  });

  return {Card: React.createFactory(Card), SuitMap: SuitMap};
});
