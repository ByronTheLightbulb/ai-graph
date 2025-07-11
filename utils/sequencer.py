import collections

class sequencer:
    def __init__(self, inp) -> None:
        # Convert keys to int and ensure all values are sets of ints
        self.deps = {int(k): set(v) for k, v in inp["deps"]}

    def generate_sequence(self) -> list[int]:
        temp_deps = {k: set(v) for k, v in self.deps.items()}
        res = []

        # Calculate in-degrees for all nodes
        in_degrees = collections.defaultdict(int)
        for k, v in temp_deps.items():
            for dep in v:
                in_degrees[dep] += 1
        
        # Initial queue: nodes with no dependencies
        # This includes nodes that are present as keys in temp_deps but have no dependencies
        # and also nodes that are only dependencies but are not themselves keys in temp_deps (they implicitly have 0 in-degree)
        queue = collections.deque([k for k, v in temp_deps.items() if not v])

        # Also add any nodes that are dependencies but not defined as keys themselves, and thus have no outgoing edges
        # and therefore effectively have 0 dependencies for sequencing purposes.
        all_nodes = set(temp_deps.keys())
        for deps_set in temp_deps.values():
            all_nodes.update(deps_set)
        
        for node_val in all_nodes:
            if node_val not in temp_deps and node_val not in in_degrees: # It's a "leaf" node, not a key, not a dependency
                queue.append(node_val)
            elif node_val in temp_deps and not temp_deps[node_val]: # It's a key with no dependencies
                 if node_val not in queue: # Avoid adding duplicates if already added
                     queue.append(node_val)

        processed_nodes = set()

        while queue:
            node = queue.popleft()
            
            if node in processed_nodes: # Skip if already processed (can happen if added multiple times)
                continue

            res.append(node)
            processed_nodes.add(node)

            # Find nodes that depend on the current node
            # Create a list of keys to iterate to avoid RuntimeError: dictionary changed size during iteration
            for k in list(temp_deps.keys()):
                if node in temp_deps[k]:
                    temp_deps[k].discard(node)
                    if not temp_deps[k]: # If all dependencies for k are met
                        queue.append(k)
        
        # Check for circular dependencies - remaining nodes in temp_deps that haven't been processed
        # This implies they still have unresolved dependencies
        if len(res) != len(all_nodes):
            remaining_deps = {k: v for k, v in temp_deps.items() if v}
            # Find nodes that were in all_nodes but not in res
            unprocessed_nodes = all_nodes - set(res)
            
            # The remaining_deps check is often sufficient, but cross-referencing with unprocessed_nodes is more robust.
            if unprocessed_nodes:
                # If there are unprocessed_nodes, and they still have dependencies in temp_deps
                # or if they are simply not processed, it indicates a cycle or an issue.
                circular_nodes = {node for node in unprocessed_nodes if node in temp_deps and temp_deps[node]}
                if not circular_nodes and unprocessed_nodes: # Case where a node might be unprocessed but its deps are met, indicating a bug
                     raise ValueError("Some nodes could not be processed, but no circular dependency detected based on remaining_deps. Unprocessed nodes: " + str(unprocessed_nodes))
                elif circular_nodes:
                     raise ValueError("Circular dependency detected: Remaining deps -> " + str(remaining_deps) + " | Unprocessed nodes likely in cycle: " + str(circular_nodes))
            elif remaining_deps: # Should not happen if all_nodes is correctly determined and checked above
                raise ValueError("Circular dependency detected: Remaining deps -> " + str(remaining_deps))


        # Final check if all nodes from the initial input (and any dependencies) are present in the result
        # This implies that the 'all_nodes' calculation should be comprehensive
        if len(res) != len(all_nodes):
             raise ValueError(f"Not all nodes were processed. Expected {len(all_nodes)}, got {len(res)}. Missing: {all_nodes - set(res)}")

        return res
 

 
 
