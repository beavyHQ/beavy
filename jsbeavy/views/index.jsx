import React from "react";
import { addExtension, getExtensions } from 'config/extensions';
import { Route } from 'react-router';
import config from 'config/config';

import UserView from 'views/UserView';
import HomeView from 'views/HomeView';

const USERS_URL = config.USERS_URL;

export default function setupViews(Application){
  addExtension('routes',
      <Route name="user" path={USERS_URL + "/:userId/"} component={UserView}>
        {getExtensions('userRoutes')}
      </Route>);
  addExtension('routes', <Route component={HomeView} path="*" />);
}
