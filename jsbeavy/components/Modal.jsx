import React from "react";
import { Link } from "react-router";
import styles from './Modal.scss';
import classnames from 'classnames';

export class Modal extends React.Component {
  propTypes: {
    isOpen: React.PropTypes.bool.isRequired,
    onRequestClose: React.PropTypes.func,
    // closeTimeoutMS: React.PropTypes.number,
    ariaHideApp: React.PropTypes.bool
  }

  defaultProps: {
    isOpen: true,
    ariaHideApp: true,
    // closeTimeoutMS: 0
  }
  render() {
    return <div className={classnames(styles.modal, this.props.isOpen ? styles.open : '')}>
            <div className={styles.modalFadeScreen}>
              <div className={styles.modalInner}>
                <div className={styles.modalClose}></div>
                <h1>{this.props.title}</h1>
                {this.props.children}
              </div>
            </div>
          </div>;
  }
}
