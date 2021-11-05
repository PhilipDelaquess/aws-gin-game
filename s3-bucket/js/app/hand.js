define(function (require) {
  "use strict";
  var _ = require('underscore'),
    React = require('react'),
    Melding = require('app/melding');

  var Hand = React.createClass({

    render: function () {
      var meldings = _.map(this.props.hand.meldings, function (melding, key) {
        return Melding({
          key: key,
          melding: melding,
          lastDraw: this.props.lastDraw,
          callback: this.props.callback
        });
      }.bind(this));
      return React.DOM.div({}, meldings);
    }
  });

  return React.createFactory(Hand);
});
