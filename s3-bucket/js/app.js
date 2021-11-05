requirejs.config({
  baseUrl: 'js/lib',
  paths: {
    jquery: 'jquery-3.1.1.min',
    react: 'react',
    reactDOM: 'react-dom.min',
    underscore: 'underscore-min',
    app: '../app'
  }
});

requirejs(
  ['app/main', 'reactDOM'],
  function (main, ReactDOM) {
    ReactDOM.render(main(), document.getElementById('content'));
});
