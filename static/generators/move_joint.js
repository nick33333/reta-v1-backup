Blockly.Python['move_to'] = function(block) {
  var value_j1 = Blockly.Python.valueToCode(block, 'j1', Blockly.Python.ORDER_ATOMIC);
  var value_j2 = Blockly.Python.valueToCode(block, 'j2', Blockly.Python.ORDER_ATOMIC);
  var value_j3 = Blockly.Python.valueToCode(block, 'j3', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'device.rotate_joint('+ value_j1 +', '+ value_j2 +', '+ value_j3 +', 0.779, wait=True)\n\n';
  return code;
};