import React from "react";
import { MainMenu, styles as MainMenuStyles } from "components/MainMenu";
import UserModal from "containers/UserModal";
import UserMenuWidget from "containers/UserMenuWidget";

import { insertExtension } from "config/extensions";
import styles from "./styles/hn_styles.scss";

// overwrite behaviour of the logo styles
Object.assign(MainMenuStyles, {logo: styles.logo, title: styles.title})

insertExtension("MainNavigationTools", 0, () => <UserMenuWidget />)

export default class Application extends React.Component {
    render() {
        return <div className={styles.hackerNews}>
                  <UserModal />
                  <MainMenu styles={MainMenuStyles} logo='http://svgporn.com/logos/ycombinator.svg'/>
                  {this.props.children}
                </div>;
    }
}
