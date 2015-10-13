
jest.autoMockOff();
//  FIXME: IMPORT DOESN'T WORK WITH JEST MOCKING PROPERLY
// import format_jsonapi_result from '../middleware/format_jsonapi_result';
const format_jsonapi_result = require('../middleware/format_jsonapi_result');

describe('format_jsonapi_result', function(){

  it("reformats simple items", function(){
    const input = {data:
                    {type: "test", id:1, attributes: {"test": "1"}}
                  },
          output = {entities: {
                        test: {
                            1: {type: "test", "test": "1", id: 1}
                        }
                      },
                    result: {data: {type: "test", id:1}}};
    expect(format_jsonapi_result(input, "result")).toEqual(output);
  });

  it("properly formats includes", function(){
    const input = {data:[
                      {type: "test", id: 1}
                    ],
                   "included": [
                    {"type": "test", id: 2, attributes: {"a": "b"}},
                    {"type": "other", id: 201, attributes: {"C": "D"}}
                   ]},
          output = {entities: {
                        test: {
                            1: {type: "test", id: 1},
                            2: {type: "test", id: 2, "a": "b"}
                          },
                        "other":{
                            201: {"type": "other", id:201, "C": "D"}
                        }
                      },
                    stream: {data: [{type: "test", id:1}]}};
    expect(format_jsonapi_result(input)).toEqual(output);
  });

  it("properly handels relationships", function(){
    const input = {data:[
                      {type: "test", id: 1,
                       "relationships": {
                          // parent is onw
                          "parent": {data: {"type": "test", id: 2, attributes: {"a": "b"}}},
                          // partners are many
                          "partners": {data: [
                              {"type": "other", id: 201, attributes: {"C": "D"}},
                              {"type": "other", id: 300, attributes: {"E": "F"}}
                            ]}
                       }
                     }
                    ]
                  },
          output = {entities: {
                        test: {
                            1: {type: "test", id: 1,
                                parent: {"type": "test", id: 2},
                                partners: [
                                  {type: "other", id: 201},
                                  {type: "other", id: 300}
                                ]},
                            2: {type: "test", id: 2, "a": "b"}
                          },
                        "other":{
                            201: {"type": "other", id:201, "C": "D"},
                            300: {"type": "other", id:300, "E": "F"}
                        }
                      },
                    stream: {data: [{type: "test", id:1}]}};
    expect(format_jsonapi_result(input, "stream")).toEqual(output);
  });
})