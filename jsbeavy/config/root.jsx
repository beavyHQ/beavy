import React        from 'react';
import { Provider } from 'react-redux';
import { createDevToolsWindow } from 'utils';
import { Route, Redirect, DefaultRoute, NotFoundRoute, Router, RoutingContext  } from "react-router";

/* eslint-disable no-multi-spaces */
// Only import from `route-handlers/*`
import { getExtensions } from "config/extensions";
import { HOME_URL } from "config/config";
import setupViews from "views";

import { ReduxRouter } from 'redux-router';

/* eslint-enable */

export default class Root extends React.Component {

  // routerHistory is provided by the client bundle to determine which
  // history to use (memory, hash, browser). routingContext, on the other hand,
  // is provided by the server and provides a full router state.
  static propTypes = {
    store          : React.PropTypes.object.isRequired,
    application    : React.PropTypes.func.isRequired,
  }

  constructor () {
    super();
  }

  renderDevTools () {
    const { DevTools, LogMonitor, DebugPanel } = require('redux-devtools/lib/react');
    if (__DEBUG_NW__) {
      createDevToolsWindow(this.props.store);
      return null;
    } else {
      return (
        <DebugPanel top left bottom key='debugPanel'>
          <DevTools store={this.props.store} monitor={LogMonitor} />
        </DebugPanel>
      );
    }
  }

  getRoutes(){
    const routes_by_path = {},
          remapRoutes = (routes, path='') => {
            for (let i = routes.length - 1; i >= 0; i--) {
              addRoute(routes[i], path)
            };
          },
          addRoute = (x, parents="") => {
            parents = parents.charAt(parents.length - 1) ? parents : parents + '/'
            let path = x.props.path.charAt(0) == "/" ? x.props.path : parents + x.props.path;
            // react router creates some weird double-slashes, which are
            // incompatible with our way of looking at urls
            // sanitise them!
            path = path.replace(/(\/\/)/, "/");
            routes_by_path[path] = x;
            if (x.props.children){
              remapRoutes(x.props.children, path)
            }
          },
          routes = getExtensions('routes');

    remapRoutes(routes);
    if (routes_by_path[HOME_URL]){
      const store = routes_by_path[HOME_URL]._store;
      store.originalProps.path = "/";
      store.props.path = "/";
      routes.push(<Redirect from={HOME_URL} to="/" />)
    } else {
      // routes.push(<Route component={HomeView} path="*" />);
    }

    return routes;

  }

  render () {
    let debugTools = null;

    if (__REDUX_DEV_TOOLS__) {
      debugTools = this.renderDevTools();
    }

    setupViews(this.props.application);

    return (
      <div>
        {debugTools}
        <Provider store={this.props.store}>
          {() =>
              <ReduxRouter>
                <Route component={this.props.application}>
                  {this.getRoutes()}
                </Route>
              </ReduxRouter>
            }
        </Provider>
      </div>
    );
  }
}
