import React from "react";
import { addExtension, getExtensions } from 'config/extensions';
import { Route } from 'react-router';
import { make_url } from 'utils';

import UserView from 'views/UserView';
import HomeView from 'views/HomeView';

export default function setupViews(Application){
  addExtension('routes',
      <Route name="user" path={make_url.users("/:userId/")} component={UserView}>
        {getExtensions('userRoutes')}
      </Route>);
  addExtension('routes', <Route component={HomeView} path="*" />);
}
