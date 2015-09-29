

export default new Promise(resolve => {
  require.ensure([], () => {
    const ProseMirror = require('react-prosemirror');
    require('prosemirror/src/convert/to_markdown');
    require('prosemirror/src/menu/inlinemenu');
    require('prosemirror/src/menu/buttonmenu');
    resolve(ProseMirror);
  });
});