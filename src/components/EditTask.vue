<template>
	<b-modal :id="'edit-task-modal-' + task.task_id" title="Update task" hide-footer hide-header>
		<h2>Edit task</h2>
		<b-form v-on:submit.prevent="onSubmit">
			<b-form-group label="Description: " label-for="form-descr-input">
				<b-form-textarea id="form-descr-input" v-model="editTaskForm.description" required></b-form-textarea>
			</b-form-group>
			<b-form-group>
				<b-form-select id="form-priority-input" v-model="editTaskForm.priority_id" :options="options" />
			</b-form-group>
			<b-row>
				<b-col lg="2"><b-button variant="outline-primary" @click="$bvModal.hide('edit-task-modal-' + task.task_id)">Cancel</b-button></b-col>
				<b-col lg="2"><b-button type="submit" variant="success">Save</b-button></b-col>
			</b-row>
		</b-form>
	</b-modal>
</template>

<script>
import axios from 'axios';
import Priorities from '../config';

export default {
	name: 'EditTask',
	props: [
		'task'
	],
	data() {
		return {
			options: Priorities,
			editTaskForm: {
				description: this.$props.task.description,
				priority_id: this.$props.task.priority_id
			}
		}
	},
	methods: { 
		updateTask(payload) {
			const path='http://127.0.0.1:5000/task/'+this.$props.task.task_id;
			axios.put(path, payload)
				.then(() => {
					this.$parent.$parent.getTasks();
				})
				.catch((error) => {
					console.log(error);
					this.$parent.$parent.getTasks();
				});
		},
		onSubmit() {
			const payload = {
				description: this.editTaskForm.description,
				priority_id: this.editTaskForm.priority_id
			};
			this.updateTask(payload);
			this.$bvModal.hide('edit-task-modal-' + this.$props.task.task_id);
		}
	},
}
</script>