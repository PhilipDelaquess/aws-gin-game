define(function (require) {
  "use strict";
  var $ = require('jquery'),
    _ = require('underscore'),
    React = require('react'),
    ReactDOM = require('reactDOM'),
    Login = require('app/login'),
    Score = require('app/score'),
    Game = require('app/game');

  var gatewayUrl = 'https://z668d08agd.execute-api.us-east-2.amazonaws.com/prod/';

  var Main = React.createClass({
    getInitialState: function () {
      return {
        player: null,
        error: null
      };
    },

    componentDidMount: function () {
      this.timer = setInterval(this.getStatus, 5000);
    },

    componentWillUnmount: function () {
      clearInterval(this.timer);
    },

    getStatus: function () {
      if (!this.state.player) {
        return;
      }
      var st = this.state.player.state;
      if (st != 'AWAITING_OPPONENT_ARRIVAL' && st != 'AWAITING_OPPONENT_ACTION') {
        return;
      }
      //var statusUrl = '/api/gin-server/';
      $.getJSON(gatewayUrl + this.state.player.id)
      .done(function (data) {
        this.setState({player: data});
      }.bind(this))
      .fail(function () {
        this.setState({error: 'Something went tilt on the server. Sorry.'});
        clearInterval(this.timer);
      }.bind(this));
    },

    userLoggedIn: function (name) {
      $.ajax({
        type: 'POST',
        url: gatewayUrl + 'new-player',
        contentType: 'text/plain',
        data: name
      }).done(function (data) {
        this.setState({player: data});
      }.bind(this));
    },

    sendCommand: function (action, card) {
      var command = {
        id: this.state.player.id,
        action: action,
        abbrev: card
      }
      $.ajax({
        type: 'POST',
        url: gatewayUrl + 'action',
        contentType: 'application/json',
        data: JSON.stringify(command)
      }).done(function (data) {
        this.setState({player: data});
      }.bind(this));
    },

    clickedDeck: function () {
      this.sendCommand('DRAW_PACK', null);
    },

    clickedDiscard: function () {
      this.sendCommand('DRAW_DISCARD', null);
    },

    clickedReject: function () {
      this.sendCommand('REJECT_INITIAL', null);
    },

    clickedCard: function (abbrev, knock) {
      this.sendCommand(knock ? 'KNOCK' : 'DISCARD', abbrev);
    },

    clickedAcknowledge: function () {
      this.sendCommand('ACKNOWLEDGE', null);
    },

    render: function () {
      if (this.state.error) {
        return React.DOM.h3({className: 'red'}, this.state.error);
      } else if (!this.state.player) {
        return Login({
          callback: this.userLoggedIn
        });
      } else if (this.state.player.state == 'AWAITING_OPPONENT_ARRIVAL') {
        return React.DOM.h3({},
          'Welcome, ' + this.state.player.name + '. Waiting for opponent to arrive...');
      } else if (this.state.player.state == 'ACKNOWLEDGE_DEAL') {
        return Score({
          callback: this.clickedAcknowledge,
          player: this.state.player
        });
      } else {
        var pState = this.state.player.state;
        var deckCallback = pState == 'NORMAL_DRAW'
          ? this.clickedDeck : null;
        var wasteCallback = _.contains(['PONE_INITIAL_DRAW', 'DEALER_INITIAL_DRAW', 'NORMAL_DRAW'], pState)
          ? this.clickedDiscard : null;
        var rejectCallback = _.contains(['PONE_INITIAL_DRAW', 'DEALER_INITIAL_DRAW'], pState)
          ? this.clickedReject : null;
        var cardCallback = pState == 'DISCARD_OR_KNOCK'
          ? this.clickedCard : null;
        return Game({
          deckCallback: deckCallback,
          wasteCallback: wasteCallback,
          rejectCallback: rejectCallback,
          cardCallback: cardCallback,
          player: this.state.player
        });
      }
    }
  });

  return React.createFactory(Main);
});
