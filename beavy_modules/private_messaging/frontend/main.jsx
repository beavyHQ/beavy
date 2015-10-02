import React from "react";
import { Link, Route } from "react-router";
import { connect } from "react-redux";
import { addExtension } from 'config/extensions';
import { make_url } from 'utils';


import { loadPMs } from './actions';
import PrivateMessagesView from './views/PrivateMessages';
import PrivateMessageView from './views/PrivateMessage';

addExtension("userNavigationItems", (function() {return <Link to={make_url.account("private_messages/")}>Private Messages</Link>;}));
addExtension("accountRoutes", <Route path="private_messages/" component={PrivateMessagesView} /> );
addExtension("accountRoutes", <Route path="private_messages/:messageId/" component={PrivateMessageView} /> );