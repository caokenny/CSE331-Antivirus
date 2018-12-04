// #include </usr/include/Python.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kmod.h>
#include <linux/unistd.h>
#include <linux/mutex.h>


MODULE_LICENSE("GPL");
MODULE_AUTHOR("Alan <ex0dus@codemuch.tech>");

unsigned long *sys_call_table = (unsigned long*) 0xdd8ae1e0;
static DEFINE_MUTEX(my_mutex);

/* This defines a pointer to the real open() syscall */
asmlinkage int (*old_open)(const char *filename, int flags, int mode);
// asmlinkage int (*old_execve) (const char *filename, char *const argv[], char *const envp[]);


/* enable use to memory page and write to it */
void
set_addr_rw(long unsigned int _addr)
{
    unsigned int level;
    pte_t *pte = lookup_address(_addr, &level);

    if (pte->pte &~ _PAGE_RW) pte->pte |= _PAGE_RW;
}

/* ensure that when cleanup occurs, make page write-protected */
void
set_addr_ro(long unsigned int _addr)
{
    unsigned int level;
    pte_t *pte = lookup_address(_addr, &level);

    pte->pte = pte->pte &~_PAGE_RW;
}


// asmlinkage int
// new_execve(const char *filename, char *const argv[], char *const envp[]) {
//     printk(KERN_ALERT "Intercepting execve(%s, %s, %s)\n", filename, argv[3], envp[0]);
//     return (*old_execve) (filename, argv, envp);
// }


asmlinkage int
new_open(const char *filename, int flags, int mode)
{

    if (!mutex_trylock(&my_mutex)) {
        printk(KERN_ALERT "MUTEX: In use by another process\n");
        return -EBUSY;
    }

    printk(KERN_INFO "Intercepting open(%s, %X, %X)\n", filename, flags, mode);

    sys_call_table[__NR_open] = old_open;

    char *argv[] = {"./antivirus", "-f", filename, NULL};
    char *envp[] = {
        "HOME=/",
        "TERM=xterm-256color",
        "USER=root",
        "SHELL=/bin/bash",
        "DISPLAY=:0",
        "PATH=/usr/bin:/bin", NULL
    };

    int result = call_usermodehelper(argv[0], argv, envp, UMH_WAIT_PROC);


    // printk(KERN_ALERT "result = %d\n", result);

    sys_call_table[__NR_open] = new_open;


    mutex_unlock(&my_mutex);
    printk(KERN_ALERT "MUTEX: unlocked\n");



    /* give execution BACK to the original syscall */
    return (*old_open)(filename, flags, mode);
    // return NULL;
}

static int __init
init(void)
{
    printk(KERN_INFO "Welcome to Kernel Town!\n");

    /* allow us to write to memory page, so that we can hijack the system call */
    set_addr_rw((unsigned long) sys_call_table);

    /* grab system call number definition from sys_call_table */
    old_open = (void *) sys_call_table[__NR_open];
    // old_execve = (void *) sys_call_table[__NR_execve];

    /* set the open symbol to our new_open system call definition */

    sys_call_table[__NR_open] = new_open;
    // sys_call_table[__NR_execve] = new_execve;

    return 0;
}

static void __exit
cleanup(void)
{
    /* set the open symbol BACK to the old open system call definition */
    sys_call_table[__NR_open] = old_open;
    // sys_call_table[__NR_execve] = old_execve;

    /* set memory page back to read-only */
    set_addr_ro((unsigned long) sys_call_table);

    printk(KERN_INFO "We are now leaving Kernel Town! Thanks for the stay!\n");
    return;
}

module_init(init);
module_exit(cleanup);
