define(function (require) {
  "use strict";

  const stage = '_STAGE_';
  const apiId = '_API_ID_';

  return {
  	gatewayUrl: 'https://' + apiId + '.execute-api.us-east-2.amazonaws.com/' + stage + '/'
  };

});
