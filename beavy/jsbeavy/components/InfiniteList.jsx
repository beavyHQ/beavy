/*eslint-disable react/no-multi-comp*/
import React, { Component, PropTypes} from 'react'
import ReactDOM from  'react-dom'
import { FormattedMessage } from 'react-intl'
import Infinite from 'react-infinite'
import map from 'lodash/collection/map'
import { fill, isEqual } from 'lodash'

class SizeReportWrapper extends Component {
  propTypes: {
    reportHeight: PropTypes.func.isRequired,
    element: PropTypes.Component.isRequired,
  }
  componentDidMount () {
    var el = ReactDOM.findDOMNode(this.refs.child)
    this.props.reportHeight(el.offsetHeight)
  }
  render () {
    return React.cloneElement(this.props.element, {ref: 'child'})
  }
}

export default class InfiniteList extends Component {

  propTypes: {
    children: PropTypes.array.isRequired,
    minimalItemHeight: PropTypes.number,
    loader: PropTypes.func.isRequired,
    isFetching: PropTypes.bool.isRequired
    // meta: PropTypes.shape({
    //   has_next: PropTypes.bool.isRequired,
    //   page: PropTypes.number.isRequired,
    //   // 'total-pages': PropTypes.number.isRequired,
    // })
  }

  constructor (props) {
    super(props)
    let minimalItemHeight = props.minimalItemHeight || 100
    this.state = {
      elementHeights: map(props.children, x => minimalItemHeight),
    }
  }

  shouldComponentUpdate (nextProps, nextState) {
    var propsChanged = !isEqual(this.props, nextProps)
    var stateChanged = this.state !== nextState
    return propsChanged || stateChanged
  }

  render () {
    return <Infinite elementHeight={this.state.elementHeights}
                     useWindowAsScrollContainer={true}
                     infiniteLoadBeginEdgeOffset={!this.props.meta.has_next ? undefined : 200}
                     onInfiniteLoad={::this.handleInfiniteLoad}
                     loadingSpinnerDelegate={this.elementInfiniteLoad()}
                     preloadBatchSize={Infinite.containerHeightScaleFactor(2)}
                     isInfiniteLoading={this.props.isFetching}
         className='infinite-list'
         scrollNumberCallback={this.scrollCallback}
         selectedItem={this.props.selectedItem}
                     >
        {map(this.props.children, (c, i) => <SizeReportWrapper key={i} element={c} reportHeight={(height) => this.reportHeight(i, height)} />
        )}
    </Infinite>
  }

  reportHeight (i, height) {
    let curHeights = this.state.elementHeights
    curHeights[i] = height
    this.setState({elementHeights: curHeights})
  }

  componentWillReceiveProps (newProps) {
    let newState = {elements: newProps.children}
    if (this.props.children.length < newProps.children.length) {
      const minimalItemHeight = newProps.minimalItemHeight || this.props.minimalItemHeight || 100
      newState.elementHeights = this.state.elementHeights.concat(
        fill(Array(newProps.children.length - this.props.children.length), minimalItemHeight))
    }
    this.setState(newState)
  }

  handleInfiniteLoad () {
    if (this.props.meta.has_next && !this.props.isFetching) {
      this.props.loader(this.props.meta.page + 1)
    }
  }

  elementInfiniteLoad () {
    return (
      <div className='infinite-list-item'>
        <FormattedMessage
          id='infinite-list-message'
          description='Infinite List Message'
          defaultMessage='Loading...' />
      </div>
    )
  }

  scrollCallback (num) {
    if (this.props.routeOnScroll) {
      // FIXME: WHAT IS ROUTE ACTIONS?
      // routeActions.setRoute('/infinite_demo/' + this.props.query + '/' + this.state.elements[num].props.data.masterid)
    }
    if (this.props.scrollCallback) {
      this.props.scrollCallback(num)
    }
  }
}
