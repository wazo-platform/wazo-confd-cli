# wazo-confd-cli
CLI tool to inspect and update wazo-confd resources


## Example usage

```shell
export TOKEN=$(wazo-auth-cli token create --auth-username <username> --auth-password = <password>)
wazo-confd-cli --token ${TOKEN} user list --tenant <tenant-uuid>
```
