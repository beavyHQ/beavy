
require("./styles/main.scss")
import modules from './app/modules';

import makeRoutes from "./app/routes";
import stores from "./app/mainStores";
import renderApplication from "./config/renderApplication";

let Application = require("module-imports?ext=.jsx&key=FRONTEND&path=./jsbeavy/app/apps/!yaml!../config.yml").default;

renderApplication(makeRoutes(Application), stores, {
  timeout: 600
});
