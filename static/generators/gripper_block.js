Blockly.Python['gripper'] = function(block) {
    var dropdown_name = block.getFieldValue('NAME');
    if (dropdown_name == 'OPEN') {
        var code = 'device.grip(False)\n\n';
    } else if (dropdown_name == 'CLOSE') {
        var code = 'device.grip(True)\n\n';
    } else {
        var code = 'device.suck(False)\n\n';
    }
    return code;
  };