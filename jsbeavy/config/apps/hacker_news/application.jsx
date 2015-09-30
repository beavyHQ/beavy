import React from "react";
import { MainMenu, styles as MainMenuStyles } from "components/MainMenu";
import UserModal from "containers/UserModal";
import UserMenuWidget from "containers/UserMenuWidget";

import { insertExtension } from "config/extensions";
import styles from "./styles/hn_styles.scss";

const customMenuStyles = Object.assign({},
                          MainMenuStyles,
                          {logo: styles.logo});
console.log(customMenuStyles);
console.log(customMenuStyles.logo);

insertExtension("MainNavigationTools", 0, () => <UserMenuWidget />)

export default class Application extends React.Component {
    render() {
        return <div className={styles.hackerNews}>
                  <UserModal />
                  <MainMenu styles={customMenuStyles} logo='http://svgporn.com/logos/ycombinator.svg'/>
                  {this.props.children}
                </div>;
    }
}
