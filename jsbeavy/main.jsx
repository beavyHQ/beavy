
require("styles/main.scss")
import modules from 'config/modules';

import makeRoutes from "config/routes";
import stores from "config/mainStores";
import renderApplication from "config/renderApplication";

let Application = require("module-imports?ext=/application.jsx&key=FRONTEND&path=config/apps/!yaml!../config.yml").default;

renderApplication(makeRoutes(Application), stores, {
  timeout: 600
});
