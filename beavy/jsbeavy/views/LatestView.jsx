import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getStoreEntity } from 'utils'
import { LATEST } from 'reducers/latest'
import { loadLatest } from 'actions/latest'
import InfiniteList from 'components/InfiniteList'

// This should be a stateless component but if it's to be
// consumed by the InfiniteList later, we'll need to add
// a ref and you can't do that on stateless components.
class Link extends Component {
  render() {
    const props = this.props
    return (
      <li key={props.key} style={{height: 350}}>
        <a target="_blank" href={props.url}>{props.title}</a>
      </li>
    )
  }
}

const LinksList = ({
  meta,
  links,
  loadMore
}) => (
  <InfiniteList
    meta={meta}
    loader={loadMore}
    minimalItemHeight={24}
  >
    {links.map(l =>
      <Link key={l.id} {...l} />
    )}
  </InfiniteList>
)

const mapStateToProps = (state) => {
  return {
    meta: state[LATEST].meta,
    links: state[LATEST].data.map((item) => {
      return getStoreEntity(state, item)
    })
  }
}

const mapDispatchToProps = (dispatch, props) => {
  return {
    loadMore: (page) => {
      console.log('loadMore', {page: page})
      dispatch(loadLatest(page))
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LinksList)

