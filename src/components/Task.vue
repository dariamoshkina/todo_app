<template>
	<tr>
		<td :id="'popover-' + task.task_id">
			{{task.description}}
			<b-popover :target="'popover-' + task.task_id" triggers="hover" placement="left">
				task_id={{task.task_id}}
			</b-popover>
		</td>
		<td>{{task.priority.name}}</td>
		<td>{{task.created_at}}</td>
		<td>
			<button type="button" class="btn btn-primary" v-b-modal="'edit-task-modal-' + task.task_id" @click="$bvModal.show('edit-task-modal-'+task.task_id)">Edit</button>			
			<EditTask v-bind:task="task"/>
		</td>
		<td>
			<button type="button" class="btn btn-danger" v-on:click="deleteTask(task.task_id)">Delete</button>
		</td>
	</tr>
</template>

<script>
import axios from 'axios';
import EditTask from './EditTask';

export default {
	name: 'Task',
	props: ['task'],
	methods: {
		deleteTask(task_id) {
			const path='http://127.0.0.1:5000/task/'+task_id;
			axios.delete(path)
				.then(() => {
					this.$parent.getTasks();
				})
				.catch((error) => {
					console.log(error);
					this.$parent.getTasks();
				});
		},
	},
	components: {
		EditTask,
	}
}
</script>

