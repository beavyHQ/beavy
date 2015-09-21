
import React from 'react';
import { getNamedExtensions } from "config/extensions";
import createBrowserHistory from 'history/lib/createBrowserHistory';

// polyfill
if(!Object.assign)
  Object.assign = React.__spread; // eslint-disable-line no-underscore-dangle

require("styles/main.scss")

import config from "config/config";
import modules from 'config/modules';

import Root from 'config/root';

// tie it all together
const Application = require("module-imports?ext=/application.jsx&path=config/apps/!grep?FRONTEND!yaml!../config.yml").default;

const target = document.getElementById('content');

import configureStore from 'stores';
import { format_jsonapi_result } from 'middleware/api';

let initData = format_jsonapi_result(window.PRELOAD.PAYLOAD.data, window.PRELOAD.PAYLOAD.key)
initData.CURRENT_USER = window.PRELOAD.CURRENT_USER;

console.log(initData);

const store  = configureStore(initData);

React.render(<Root routerHistory={createBrowserHistory()}
                   application={Application}
                   store={store} />, target);
