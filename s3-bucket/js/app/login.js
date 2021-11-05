define(function (require) {
  "use strict";
  var React = require('react');

  var Login = React.createClass({
    getInitialState: function () {
      return {name: ''};
    },

    nameChanged: function (event) {
      this.setState({name: event.target.value});
    },

    buttonPressed: function (event) {
      var name = this.state.name;
      this.props.callback(name);
    },

    render: function () {
      return React.DOM.div({},
        React.DOM.span({}, 'What is your name?  '),
        React.DOM.input({
          value: this.state.name,
          onChange: this.nameChanged
        }),
        React.DOM.button({
          disabled: this.state.name.length == 0,
          onClick: this.buttonPressed
        }, 'Let\'s Play Gin!')
      );
    }
  });

  return React.createFactory(Login);

});
