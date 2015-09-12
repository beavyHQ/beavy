
require("./styles/main.scss")
import modules from './app/modules';

import makeRoutes from "./app/routes";
import stores from "./app/mainStores";
import renderApplication from "./config/renderApplication";

let Application = require("module-imports?ext=/application.jsx&key=FRONTEND&path=./jsbeavy/config/apps/!yaml!../config.yml").default;

renderApplication(makeRoutes(Application), stores, {
  timeout: 600
});
