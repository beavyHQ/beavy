import React from 'react';

// polyfill
if(!Object.assign)
  Object.assign = React.__spread; // eslint-disable-line no-underscore-dangle

require("styles/main.scss")

import config from "config/config";
import modules from 'config/modules';

console.log(config.USERS_URL)

import makeRoutes from "config/routes";
import stores from "config/mainStores";
import renderApplication from "config/renderApplication";

let Application = require("module-imports?ext=/application.jsx&path=config/apps/!grep?FRONTEND!yaml!../config.yml").default;

renderApplication(makeRoutes(Application), stores, {
  timeout: 600
});
