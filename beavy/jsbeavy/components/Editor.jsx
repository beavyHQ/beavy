export default new Promise(resolve => {
  require.ensure([], () => {
    const ProseMirror = require('react-prosemirror').default
    require('prosemirror/dist/markdown')
    require('prosemirror/dist/menu/menubar')
    resolve(ProseMirror)
  })
})
