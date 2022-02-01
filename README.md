# wazo-confd-cli
CLI tool to inspect and update wazo-confd resources


## Example usage

### Listing resources

```shell
export TOKEN=$(wazo-auth-cli token create --auth-username <username> --auth-password = <password>)
wazo-confd-cli --token ${TOKEN} user list --tenant <tenant-uuid>
```


### Associating resources

```shell
wazo-confd-cli --token ${TOKEN} endpoint sip add --template <template-uuid> <endpoint-uuid>
```
