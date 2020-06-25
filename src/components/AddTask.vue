<template>
	<b-form v-on:submit.prevent="onSubmit">
		<b-row align-v="center">
		<b-col cols="6">
			<b-form-input type="text" v-model="addTaskForm.description" placeholder="Description" required/>
		</b-col>
		<b-col cols="4">
			<b-form-select v-model="addTaskForm.priority_id" :options="options" />
		</b-col>
		<b-col cols="2">
			<b-button type="submit" variant="success">Add task</b-button>
		</b-col>
		</b-row>		
	</b-form>
</template>

<script>
import axios from 'axios';
import Priorities from '../config';

export default {
	name: "AddTask",
	data() {
		return {
			options: Priorities,
			addTaskForm: {
				description: '',
				priority_id: 2
			}
		};
	},
	methods: {
		addTask(payload) {
			const path='http://127.0.0.1:5000/task';
			axios.post(path, payload)
				.then(() => {
					this.$parent.getTasks();
				})
				.catch((error) => {
					console.log(error);
					this.$parent.getTasks();
				});
		},
		initForm() {
			this.addTaskForm.description = '';
			this.addTaskForm.priority_id = 2;
		},
		onSubmit() {
			const payload = {
				description: this.addTaskForm.description,
				priority_id: this.addTaskForm.priority_id
			};
			this.initForm();
			this.addTask(payload);
		}
	}
}
</script>