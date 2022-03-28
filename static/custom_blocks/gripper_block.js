Blockly.Blocks['gripper'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Gripper")
          .appendField(new Blockly.FieldDropdown([["open","OPEN"], ["close","CLOSE"], ["off","OFF"]]), "NAME");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(290);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };