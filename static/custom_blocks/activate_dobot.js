Blockly.Blocks['activate_robot'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Activate Robot");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(135);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };