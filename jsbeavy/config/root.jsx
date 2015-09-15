import React        from 'react';
import { Provider } from 'react-redux';
import invariant    from 'invariant';
import { Router, RoutingContext } from 'react-router';
import { createDevToolsWindow } from 'utils';
import { DevTools, LogMonitor, DebugPanel } from 'redux-devtools/lib/react';

import { Route, DefaultRoute, NotFoundRoute } from "react-router";

/* eslint-disable no-multi-spaces */
// Only import from `route-handlers/*`
import { getExtensions } from "config/extensions";
import setupViews from "views";

/* eslint-enable */

export default class Root extends React.Component {

  // routerHistory is provided by the client bundle to determine which
  // history to use (memory, hash, browser). routingContext, on the other hand,
  // is provided by the server and provides a full router state.
  static propTypes = {
    store          : React.PropTypes.object.isRequired,
    application    : React.PropTypes.func.isRequired,
    routerHistory  : React.PropTypes.object,
    routingContext : React.PropTypes.object
  }

  constructor () {
    super();
  }

  renderDevTools () {
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

  renderRouter () {
    invariant(
      this.props.routingContext || this.props.routerHistory,
      '<Root /> needs either a routingContext or routerHistory to render.'
    );



    if (this.props.routingContext) {
      return <RoutingContext {...this.props.routingContext} />;
    } else {
      return <Router history={this.props.routerHistory}>
                <Route name="app" path="/" component={this.props.application}>
                  {getExtensions('routes')}
                </Route>
              </Router>;
    }
  }

  render () {
    let debugTools = null;

    if (__REDUX_DEV_TOOLS__) {
      debugTools = this.renderDevTools();
    }

    return (
      <div>
        {debugTools}
        <Provider store={this.props.store}>
          {() => this.renderRouter()}
        </Provider>
      </div>
    );
  }
}
