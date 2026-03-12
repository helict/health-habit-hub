// Four groups of habit donors:
// - Open(-ended) task: donor is only asked to describe their habit in their own words.
// - Closed(-ended) task: donor should also mark contexts.
// - Closed(-ended) description: donor is given an explanation of the experiment.
// - Open(-ended) description: donor is not provided with an explanation before donating a habit.
export class ExperimentGroup {
  constructor(closedTask, closedDescription) {
    this.closedTask = closedTask;
    this.closedDescription = closedDescription;
  }

  toString() {
    const taskString = this.closedTask ? 'CLOSED_TASK' : 'OPEN_TASK';
    const descriptionString = this.closedDescription ? 'CLOSED_DESCRIPTION' : 'OPEN_DESCRIPTION';
    return `${taskString}_${descriptionString}`;
  }

  static random() {
    const closedTask = Math.random() < 0.5;
    const closedDesc = Math.random() < 0.5;
    return new ExperimentGroup(closedTask, closedDesc);
  }

  static fromString(str) {
    const match = str
      .toUpperCase()
      .match(/^(OPEN|CLOSED)_TASK_(OPEN|CLOSED)_DESC(RIPTION)?$/);
    if (!match) {
      throw new Error(`Invalid experiment group string: ${str}`);
    }
    return new ExperimentGroup(match[1] === 'CLOSED', match[2] === 'CLOSED');
  }

  static fromObject(obj) {
    return new ExperimentGroup(obj.closedTask, obj.closedDescription);
  }
}

// explizite Liste aller vier Gruppen
export const ALL_EXPERIMENT_GROUPS = [
  new ExperimentGroup(false, false), // OPEN_TASK_OPEN_DESCRIPTION
  new ExperimentGroup(false, true),  // OPEN_TASK_CLOSED_DESCRIPTION
  new ExperimentGroup(true, false),  // CLOSED_TASK_OPEN_DESCRIPTION
  new ExperimentGroup(true, true),   // CLOSED_TASK_CLOSED_DESCRIPTION
];
