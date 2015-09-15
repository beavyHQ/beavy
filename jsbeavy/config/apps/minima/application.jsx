import React from "react";
import { MainMenu } from "components/MainMenu";
import UserModal from "containers/UserModal";
import UserMenuWidget from "containers/UserMenuWidget";

import { insertExtension } from "config/extensions";

insertExtension("MainNavigationTools", 0, () => <UserMenuWidget />)

export default class Application extends React.Component {
    render() {
        return <div>
                  <UserModal />
                  <MainMenu logo='http://svgporn.com/logos/kong.svg'/>
                  {this.props.children}
                </div>;
    }
}
