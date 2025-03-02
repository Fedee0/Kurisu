from datetime import datetime
from typing import TYPE_CHECKING

from discord import Member, User
from discord.utils import format_dt

from .managerbase import BaseManager

if TYPE_CHECKING:
    from typing import Optional
    from . import OptionalMember

action_messages = {
    'warn': ('\N{WARNING SIGN}', 'Warn', 'warned {}'),
    'ban': ('\N{NO ENTRY}', 'Ban', 'banned {}'),
    'timeban': ('\N{NO ENTRY}', 'Time ban', 'banned {}'),
    'silentban': ('\N{NO ENTRY}', 'Silent ban', 'banned {}'),
    'softban': ('\N{NO ENTRY}', 'Soft-ban', 'soft-banned {}'),
    'unban': ('\N{WARNING SIGN}', 'Unban', 'unbanned {}'),
    'kick': ('\N{WOMANS BOOTS}', 'Kick', 'kicked {}'),
    'timeout': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Timeout', 'timed out {}'),
    'no-timeout': ('\N{SPEAKER}', 'Timeout Removed', 'removed a timeout from {}'),
    # specific role changes
    'mute': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Mute', 'muted {}'),
    'unmute': ('\N{SPEAKER}', 'Unmute', 'unmuted {}'),
    'time-mute': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Time Mute', 'muted {}'),
    'take-help': ('\N{NO ENTRY SIGN}', 'Help access taken', 'took help access from {}'),
    'give-help': ('\N{HEAVY LARGE CIRCLE}', 'Help access restored', 'restored help access for {}'),
    'meta-mute': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Meta muted', 'meta muted {}'),
    'meta-unmute': ('\N{SPEAKER}', 'Meta unmute', 'meta unmuted {}'),
    'appeals-mute': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Appeals muted', 'appeals muted {}'),
    'appeals-unmute': ('\N{SPEAKER}', 'Appeals unmute', 'appeals unmuted {}'),

    'help-mute': ('\N{SPEAKER WITH CANCELLATION STROKE}', 'Help mute', 'removed speak access in help channels from {}'),
    'help-unmute': ('\N{SPEAKER}', 'Help unmute', 'help unmuted {}'),

    'give-art': ('\N{HEAVY LARGE CIRCLE}', 'Art access restore', 'restored art access for {}'),
    'take-art': ('\N{NO ENTRY SIGN}', 'Art access taken', 'took art access from {}'),

    'give-tech': ('\N{HEAVY LARGE CIRCLE}', 'Tech access restore', 'restored tech access for {}'),
    'take-tech': ('\N{NO ENTRY SIGN}', 'Tech access taken', 'took tech access from {}'),

    'give-elsewhere': ('\N{HEAVY LARGE CIRCLE}', 'Elsewhere access restored', 'restored elsewhere access for {}'),
    'take-elsewhere': ('\N{NO ENTRY SIGN}', 'Elsewhere access taken', 'took elsewhere access from {}'),

    'no-embed': ('\N{NO ENTRY SIGN}', 'Permission Taken', 'removed embed permissions from {}'),
    'embed': ('\N{HEAVY LARGE CIRCLE}', 'Permission Restored', 'restored embed permissions for {}'),

    'probate': ('\N{NO ENTRY SIGN}', 'Probated', 'probated {}'),
    'unprobate': ('\N{HEAVY LARGE CIRCLE}', 'Un-probated', 'un-probated {}'),

    'tempstream': ('\N{HEAVY LARGE CIRCLE}', 'Permission Granted', 'granted streaming permissions to {}'),
    'no-tempstream': ('\N{NO ENTRY SIGN}', 'Permission Revoked', 'revoked streaming permissions from {}'),

    'take-memes': ('\N{NO ENTRY SIGN}', 'Permission Revoked', 'revoked meme permissions from {}'),
    'nou': ('\N{NO ENTRY SIGN}', 'Sent to the void', 'sent {} to the void'),
    'unnou': ('\N{HEAVY LARGE CIRCLE}', 'Retrieved from the void', 'retrieved {} from the void'),

    # non-specific role changes
    'watch': ('\N{EYES}', 'Watch', 'put {} on watch.'),
    'unwatch': ('\N{CROSS MARK}', 'Unwatch', 'removed {} from watch.'),
    'add-perm-role': ('\N{BLACK QUESTION MARK ORNAMENT}', 'Add role', 'added a permanent role to {}'),
    'add-temp-role': ('\N{BLACK QUESTION MARK ORNAMENT}', 'Add role', 'added a temporary role to {}'),
    'remove-role': ('\N{BLACK QUESTION MARK ORNAMENT}', 'Remove role', 'removed a role from {}'),
}


class UserLogManager(BaseManager):
    """Manages posting logs."""

    async def post_action_log(self, author: 'Member | User | OptionalMember',
                              target: 'Member | User | OptionalMember', kind: str, *, reason: 'Optional[str]' = None,
                              until: 'Optional[datetime]' = None):
        member = target if isinstance(target, (Member, User)) else target.member
        emoji, action, action_description = action_messages[kind]
        target_str = f'<@!{target.id}>'
        if member:
            target_str += ' | ' + str(member)
        msg = [f'{emoji} **{action}**: <@!{author.id}> {action_description.format(target_str)}']
        if until:
            now = datetime.now(self.bot.tz)
            msg[0] += f' for {until - now}, until {format_dt(until)}'
        msg.append(f'🏷 __User ID__: {target.id}')
        if reason:
            msg.append(f'\N{PENCIL} __Reason__: {reason}')
        else:
            msg.append('\N{PENCIL} __Reason__: No reason provided')
        msg_final = '\n'.join(msg)
        await self.bot.channels['mod-logs'].send(msg_final)
        if 'ban' in kind or 'kick' in kind:
            await self.bot.channels['server-logs'].send(msg_final)
